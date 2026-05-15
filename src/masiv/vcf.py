from __future__ import annotations

from pathlib import Path

from masiv.exceptions import VcfParseError
from masiv.models import SampleCall, Variant, VcfHeader, VcfParseResult

VCF_FIXED_COLUMNS = ["#CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO"]


def parse_vcf_file(path: str | Path) -> VcfParseResult:
    input_path = Path(path)
    return parse_vcf_text(input_path.read_text(), source_file=str(input_path))


def parse_vcf_text(text: str, source_file: str | None = None) -> VcfParseResult:
    metadata: dict[str, list[str]] = {}
    samples: list[str] = []
    variants: list[Variant] = []
    column_header_seen = False
    genome_build: str | None = None

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("##"):
            key, value = _parse_metadata_line(line)
            metadata.setdefault(key, []).append(value)
            genome_build = genome_build or _extract_genome_build(key, value)
            continue
        if line.startswith("#"):
            columns = line.split("\t")
            _validate_header_columns(columns)
            samples = columns[9:]
            column_header_seen = True
            continue
        if not column_header_seen:
            raise VcfParseError("VCF record encountered before column header")

        variants.append(
            _parse_record(
                line=line,
                line_number=line_number,
                samples=samples,
                genome_build=genome_build,
                source_file=source_file,
            )
        )

    if not column_header_seen:
        raise VcfParseError("VCF column header is missing")

    return VcfParseResult(
        header=VcfHeader(metadata=metadata, samples=samples, genome_build=genome_build),
        variants=variants,
    )


def _parse_metadata_line(line: str) -> tuple[str, str]:
    body = line[2:]
    if "=" not in body:
        return body, ""
    key, value = body.split("=", 1)
    return key, value


def _extract_genome_build(key: str, value: str) -> str | None:
    if key == "reference" and value in {"GRCh37", "GRCh38", "hg19", "hg38"}:
        return value
    if key == "contig" and "assembly=" in value:
        after = value.split("assembly=", 1)[1]
        return after.split(",", 1)[0].rstrip(">")
    return None


def _validate_header_columns(columns: list[str]) -> None:
    if columns[:8] != VCF_FIXED_COLUMNS:
        raise VcfParseError("VCF column header must start with standard fixed columns")
    if len(columns) > 8 and columns[8] != "FORMAT":
        raise VcfParseError("VCF sample columns require a FORMAT column")


def _parse_record(
    line: str,
    line_number: int,
    samples: list[str],
    genome_build: str | None,
    source_file: str | None,
) -> Variant:
    columns = line.split("\t")
    if len(columns) < 8:
        raise VcfParseError(f"VCF record on line {line_number} has fewer than 8 columns")
    if samples and len(columns) != 9 + len(samples):
        raise VcfParseError(f"VCF sample column count mismatch on line {line_number}")

    chromosome, pos_text, id_text, ref, alt_text, qual_text, filter_text, info_text = columns[:8]
    try:
        position = int(pos_text)
    except ValueError as error:
        raise VcfParseError(f"VCF POS on line {line_number} is not an integer") from error

    sample_calls: list[SampleCall] = []
    if samples:
        format_keys = columns[8].split(":") if columns[8] not in {"", "."} else []
        for sample_id, sample_text in zip(samples, columns[9:], strict=True):
            sample_values = sample_text.split(":") if sample_text not in {"", "."} else []
            fields = dict(zip(format_keys, sample_values, strict=False))
            sample_calls.append(
                SampleCall(sample_id=sample_id, fields=fields, genotype=fields.get("GT"))
            )

    return Variant(
        chromosome=chromosome,
        position=position,
        ids=[] if id_text == "." else id_text.split(";"),
        ref=ref,
        alts=alt_text.split(","),
        qual=None if qual_text == "." else float(qual_text),
        filters=[] if filter_text in {".", "PASS"} else filter_text.split(";"),
        info=_parse_info(info_text),
        samples=sample_calls,
        genome_build=genome_build,
        source_file=source_file,
        source_line=line_number,
    )


def _parse_info(info_text: str) -> dict[str, str | bool]:
    if info_text in {"", "."}:
        return {}

    info: dict[str, str | bool] = {}
    for item in info_text.split(";"):
        if not item:
            continue
        if "=" not in item:
            info[item] = True
            continue
        key, value = item.split("=", 1)
        info[key] = value
    return info
