from pathlib import Path

import pytest

from masiv.exceptions import VcfParseError
from masiv.vcf import parse_vcf_file, parse_vcf_text

FIXTURE = Path(__file__).parent / "fixtures" / "sample.vcf"


def test_parse_vcf_preserves_header_samples_and_genome_build() -> None:
    result = parse_vcf_file(FIXTURE)

    assert result.header.samples == ["proband", "mother"]
    assert result.header.genome_build == "GRCh38"
    assert result.header.metadata["fileformat"] == ["VCFv4.3"]
    assert len(result.variants) == 2


def test_parse_vcf_record_preserves_info_format_and_provenance() -> None:
    result = parse_vcf_file(FIXTURE)
    variant = result.variants[0]

    assert variant.chromosome == "1"
    assert variant.position == 12345
    assert variant.ids == ["rs1"]
    assert variant.ref == "A"
    assert variant.alts == ["G"]
    assert variant.qual == 99.7
    assert variant.filters == []
    assert variant.info == {"DP": "20", "SOMATIC": True}
    assert variant.samples[0].sample_id == "proband"
    assert variant.samples[0].genotype == "0/1"
    assert variant.samples[0].fields == {"GT": "0/1", "AD": "10,8", "DP": "18"}
    assert variant.samples[1].sample_id == "mother"
    assert variant.genome_build == "GRCh38"
    assert variant.source_file == str(FIXTURE)
    assert variant.source_line == 10


def test_parse_vcf_handles_multiallelic_missing_quality_and_filter() -> None:
    result = parse_vcf_file(FIXTURE)
    variant = result.variants[1]

    assert variant.ids == []
    assert variant.alts == ["T", "G"]
    assert variant.qual is None
    assert variant.filters == ["q10"]
    assert variant.samples[0].genotype == "1/2"


def test_parse_vcf_text_rejects_record_before_header() -> None:
    with pytest.raises(VcfParseError, match="column header"):
        parse_vcf_text("1\t123\t.\tA\tG\t.\tPASS\t.\n")


def test_parse_vcf_text_rejects_wrong_sample_count() -> None:
    text = (
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\ts1\ts2\n"
        "1\t1\t.\tA\tG\t.\tPASS\t.\tGT\t0/1\n"
    )

    with pytest.raises(VcfParseError, match="sample column count"):
        parse_vcf_text(text)
