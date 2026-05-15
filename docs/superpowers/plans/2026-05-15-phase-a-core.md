# Phase A MASIV Core Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Phase A deterministic MASIV core: VCF-first normalization, JSON-serializable Pydantic contracts, rule-pack resolution, ACMG/point combiners, conflict detection, and a thin CLI.

**Architecture:** Create a small Python package under `src/masiv` with focused modules for models, VCF parsing, rule resolution, classification combination, and CLI commands. Keep all clinical criterion assignment out of Phase A; tests use synthetic `CriterionResult` fixtures to validate contracts and combiners.

**Tech Stack:** Python, Pydantic v2, pytest, Ruff, mypy, argparse, stdlib JSON/pathlib.

---

## File structure

- Create `pyproject.toml` — package metadata, dependencies, dev tools, CLI entry point, Ruff/mypy/pytest config.
- Create `src/masiv/__init__.py` — package version export.
- Create `src/masiv/exceptions.py` — typed exceptions for VCF parsing, rule packs, and combiner failures.
- Create `src/masiv/models.py` — Pydantic enums/models for variants, evidence, criteria, rules, manifests, and classification outputs.
- Create `src/masiv/vcf.py` — VCF/VCF-like parser and normalization into `Variant` objects.
- Create `src/masiv/rules.py` — JSON rule-pack loading and precedence resolution.
- Create `src/masiv/combiner.py` — point scoring, ACMG categorical classification, and conflict detection.
- Create `src/masiv/cli.py` — `parse` and `combine` subcommands.
- Create `tests/fixtures/sample.vcf` — small VCF with metadata, two samples, INFO, FORMAT, and multi-allelic ALT.
- Create `tests/fixtures/criteria_likely_pathogenic.json` — synthetic criteria input for CLI combine.
- Create `tests/test_models.py` — model serialization and validation tests.
- Create `tests/test_vcf.py` — VCF parser tests.
- Create `tests/test_rules.py` — rule-pack resolution tests.
- Create `tests/test_combiner.py` — point, ACMG category, modified strength, conflict tests.
- Create `tests/test_cli.py` — CLI parse/combine tests.
- Modify `CLAUDE.md` — replace unverified command caveat after commands pass.

This repository is not currently git-managed, so plan steps do not include `git commit`. If a git repository is initialized later, commit after each task with the files listed in that task.

---

### Task 1: Package scaffold and tool configuration

**Files:**
- Create: `pyproject.toml`
- Create: `src/masiv/__init__.py`
- Create: `src/masiv/exceptions.py`

- [ ] **Step 1: Write package metadata and tool config**

Create `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "masiv"
version = "0.1.0"
description = "Multi Agent System for Interpreting Variants deterministic ACMG core"
requires-python = ">=3.11"
dependencies = [
  "pydantic>=2.8,<3",
]

[project.optional-dependencies]
dev = [
  "mypy>=1.11",
  "pytest>=8.0",
  "ruff>=0.6",
]

[project.scripts]
masiv = "masiv.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]

[tool.ruff]
line-length = 100
target-version = "py311"
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.mypy]
python_version = "3.11"
strict = true
mypy_path = "src"
packages = ["masiv"]
```

- [ ] **Step 2: Create package init**

Create `src/masiv/__init__.py`:

```python
__version__ = "0.1.0"
```

- [ ] **Step 3: Create typed exceptions**

Create `src/masiv/exceptions.py`:

```python
class MasivError(Exception):
    """Base exception for MASIV."""


class VcfParseError(MasivError):
    """Raised when VCF input cannot be parsed safely."""


class RulePackError(MasivError):
    """Raised when a rule pack is malformed or cannot be resolved."""


class CombinerError(MasivError):
    """Raised when criterion results cannot be combined."""
```

- [ ] **Step 4: Install package with dev dependencies**

Run:

```bash
python -m pip install -e /data/code/mavif[dev]
```

Expected: package installs successfully, including pytest, Ruff, mypy, and Pydantic.

- [ ] **Step 5: Verify package imports**

Run:

```bash
python -c "import masiv; print(masiv.__version__)"
```

Expected: prints `0.1.0`.

---

### Task 2: Pydantic contracts for variants, criteria, rules, and classifications

**Files:**
- Create: `src/masiv/models.py`
- Test: `tests/test_models.py`

- [ ] **Step 1: Write failing model tests**

Create `tests/test_models.py`:

```python
from masiv.models import (
    Classification,
    ClassificationResult,
    CriterionDirection,
    CriterionResult,
    CriterionStatus,
    EvidenceRecord,
    EvidenceStrength,
    SampleCall,
    SourceManifestEntry,
    Variant,
    VariantContext,
)


def test_variant_round_trip_preserves_vcf_provenance() -> None:
    variant = Variant(
        chromosome="1",
        position=12345,
        ids=["rs1"],
        ref="A",
        alts=["G"],
        qual=99.7,
        filters=[],
        info={"DP": "20", "SOMATIC": True},
        samples=[
            SampleCall(
                sample_id="proband",
                fields={"GT": "0/1", "DP": "18"},
                genotype="0/1",
            )
        ],
        genome_build="GRCh38",
        source_file="input.vcf",
        source_line=5,
    )

    restored = Variant.model_validate_json(variant.model_dump_json())

    assert restored.chromosome == "1"
    assert restored.position == 12345
    assert restored.alts == ["G"]
    assert restored.info["SOMATIC"] is True
    assert restored.samples[0].sample_id == "proband"
    assert restored.samples[0].genotype == "0/1"
    assert restored.genome_build == "GRCh38"
    assert restored.source_line == 5


def test_criterion_result_preserves_evidence_and_context() -> None:
    result = CriterionResult(
        criterion="PM2",
        direction=CriterionDirection.PATHOGENIC,
        strength=EvidenceStrength.SUPPORTING,
        status=CriterionStatus.MET,
        rule_pack="clingen_svi_generic",
        rule_version="PM2_SVI_2020",
        variant_context=VariantContext(
            genome_build="GRCh38",
            transcript="NM_000000.1",
            gene="GENE",
            disease="MONDO:0000001",
            inheritance="autosomal_dominant",
        ),
        evidence=[
            EvidenceRecord(
                source="gnomAD",
                version="v4.1",
                field="max_faf95",
                value=0.000001,
                threshold="below PM2 supporting threshold",
                accession="1-12345-A-G",
                notes="synthetic fixture",
            )
        ],
        reasoning="Absent or rare in population data.",
        limitations=["Disease-specific threshold unavailable."],
    )

    restored = CriterionResult.model_validate_json(result.model_dump_json())

    assert restored.criterion == "PM2"
    assert restored.strength is EvidenceStrength.SUPPORTING
    assert restored.evidence[0].source == "gnomAD"
    assert restored.variant_context.gene == "GENE"
    assert restored.limitations == ["Disease-specific threshold unavailable."]


def test_classification_result_preserves_manifest_and_not_assessed() -> None:
    result = ClassificationResult(
        classification=Classification.VUS,
        acmg_rule="no_combination_met",
        point_total=0,
        criteria_used=[],
        criteria_withheld=[],
        criteria_not_assessed=["PS2", "PS3"],
        conflicts=[],
        missing_evidence=["trio data", "functional assay evidence"],
        source_manifest=[
            SourceManifestEntry(name="base_acmg_2015", version="2015", kind="guideline")
        ],
    )

    restored = ClassificationResult.model_validate_json(result.model_dump_json())

    assert restored.classification is Classification.VUS
    assert restored.criteria_not_assessed == ["PS2", "PS3"]
    assert restored.source_manifest[0].name == "base_acmg_2015"
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
python -m pytest tests/test_models.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'masiv.models'` or missing model names.

- [ ] **Step 3: Implement models**

Create `src/masiv/models.py`:

```python
from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

ACMG_CRITERIA = {
    "PVS1",
    "PS1",
    "PS2",
    "PS3",
    "PS4",
    "PM1",
    "PM2",
    "PM3",
    "PM4",
    "PM5",
    "PM6",
    "PP1",
    "PP2",
    "PP3",
    "PP4",
    "PP5",
    "BA1",
    "BS1",
    "BS2",
    "BS3",
    "BS4",
    "BP1",
    "BP2",
    "BP3",
    "BP4",
    "BP5",
    "BP6",
    "BP7",
}


class MasivModel(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=False)


class CriterionDirection(StrEnum):
    PATHOGENIC = "pathogenic"
    BENIGN = "benign"


class EvidenceStrength(StrEnum):
    SUPPORTING = "supporting"
    MODERATE = "moderate"
    STRONG = "strong"
    VERY_STRONG = "very_strong"
    STAND_ALONE = "stand_alone"


class CriterionStatus(StrEnum):
    MET = "met"
    NOT_MET = "not_met"
    NOT_ASSESSED = "not_assessed"
    WITHHELD = "withheld"


class Classification(StrEnum):
    PATHOGENIC = "Pathogenic"
    LIKELY_PATHOGENIC = "Likely Pathogenic"
    VUS = "VUS"
    LIKELY_BENIGN = "Likely Benign"
    BENIGN = "Benign"


class SampleCall(MasivModel):
    sample_id: str
    fields: dict[str, str] = Field(default_factory=dict)
    genotype: str | None = None


class DiseaseContext(MasivModel):
    disease: str | None = None
    disease_id: str | None = None
    inheritance: str | None = None
    phenotypes: list[str] = Field(default_factory=list)


class VariantContext(MasivModel):
    genome_build: str | None = None
    transcript: str | None = None
    gene: str | None = None
    disease: str | None = None
    inheritance: str | None = None


class Variant(MasivModel):
    chromosome: str
    position: int = Field(gt=0)
    ids: list[str] = Field(default_factory=list)
    ref: str
    alts: list[str]
    qual: float | None = None
    filters: list[str] = Field(default_factory=list)
    info: dict[str, Any] = Field(default_factory=dict)
    samples: list[SampleCall] = Field(default_factory=list)
    genome_build: str | None = None
    disease_context: DiseaseContext | None = None
    transcript: str | None = None
    gene: str | None = None
    source_file: str | None = None
    source_line: int | None = Field(default=None, gt=0)

    @field_validator("alts")
    @classmethod
    def require_alt(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("at least one ALT allele is required")
        return value


class VcfHeader(MasivModel):
    metadata: dict[str, list[str]] = Field(default_factory=dict)
    samples: list[str] = Field(default_factory=list)
    genome_build: str | None = None


class VcfParseResult(MasivModel):
    header: VcfHeader
    variants: list[Variant]


class EvidenceRecord(MasivModel):
    source: str
    version: str | None = None
    field: str | None = None
    value: Any = None
    threshold: Any = None
    accession: str | None = None
    url: str | None = None
    notes: str | None = None


class SourceManifestEntry(MasivModel):
    name: str
    version: str | None = None
    kind: str
    url: str | None = None
    accessed: str | None = None


class CriterionResult(MasivModel):
    criterion: str
    direction: CriterionDirection
    strength: EvidenceStrength
    status: CriterionStatus
    rule_pack: str
    rule_version: str
    variant_context: VariantContext = Field(default_factory=VariantContext)
    evidence: list[EvidenceRecord] = Field(default_factory=list)
    reasoning: str | None = None
    limitations: list[str] = Field(default_factory=list)

    @field_validator("criterion")
    @classmethod
    def criterion_must_be_acmg_code(cls, value: str) -> str:
        normalized = value.upper()
        if normalized not in ACMG_CRITERIA:
            raise ValueError(f"unsupported ACMG criterion: {value}")
        return normalized


class CriterionRule(MasivModel):
    criterion: str
    direction: CriterionDirection
    default_strength: EvidenceStrength
    enabled: bool = True
    rule_version: str
    thresholds: dict[str, Any] = Field(default_factory=dict)
    citations: list[str] = Field(default_factory=list)
    notes: str | None = None

    @field_validator("criterion")
    @classmethod
    def criterion_must_be_acmg_code(cls, value: str) -> str:
        normalized = value.upper()
        if normalized not in ACMG_CRITERIA:
            raise ValueError(f"unsupported ACMG criterion: {value}")
        return normalized


class RulePack(MasivModel):
    name: str
    version: str
    precedence: int
    criteria: dict[str, CriterionRule] = Field(default_factory=dict)
    source_manifest: list[SourceManifestEntry] = Field(default_factory=list)


class OverriddenValue(MasivModel):
    criterion: str
    field: str
    old_rule_pack: str
    old_value: Any
    new_rule_pack: str
    new_value: Any


class RuleResolution(MasivModel):
    active_rules: dict[str, CriterionRule]
    rule_packs: list[str]
    overrides: list[OverriddenValue] = Field(default_factory=list)
    source_manifest: list[SourceManifestEntry] = Field(default_factory=list)


class ClassificationResult(MasivModel):
    classification: Classification
    acmg_rule: str
    point_total: int
    criteria_used: list[str] = Field(default_factory=list)
    criteria_withheld: list[str] = Field(default_factory=list)
    criteria_not_assessed: list[str] = Field(default_factory=list)
    conflicts: list[str] = Field(default_factory=list)
    missing_evidence: list[str] = Field(default_factory=list)
    source_manifest: list[SourceManifestEntry] = Field(default_factory=list)
```

- [ ] **Step 4: Run model tests**

Run:

```bash
python -m pytest tests/test_models.py -v
```

Expected: PASS.

---

### Task 3: VCF parser and normalization

**Files:**
- Create: `src/masiv/vcf.py`
- Create: `tests/fixtures/sample.vcf`
- Test: `tests/test_vcf.py`

- [ ] **Step 1: Create VCF fixture**

Create `tests/fixtures/sample.vcf`:

```text
##fileformat=VCFv4.3
##reference=GRCh38
##contig=<ID=1,assembly=GRCh38>
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
##INFO=<ID=SOMATIC,Number=0,Type=Flag,Description="Somatic flag fixture">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read depth">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	proband	mother
1	12345	rs1	A	G	99.7	PASS	DP=20;SOMATIC	GT:AD:DP	0/1:10,8:18	0/0:20,0:20
1	12346	.	C	T,G	.	q10	DP=12	GT:DP	1/2:12	0/1:11
```

- [ ] **Step 2: Write failing parser tests**

Create `tests/test_vcf.py`:

```python
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
    text = "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\ts1\ts2\n1\t1\t.\tA\tG\t.\tPASS\t.\tGT\t0/1\n"

    with pytest.raises(VcfParseError, match="sample column count"):
        parse_vcf_text(text)
```

- [ ] **Step 3: Run parser tests to verify they fail**

Run:

```bash
python -m pytest tests/test_vcf.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'masiv.vcf'`.

- [ ] **Step 4: Implement parser**

Create `src/masiv/vcf.py`:

```python
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
```

- [ ] **Step 5: Run parser tests**

Run:

```bash
python -m pytest tests/test_vcf.py -v
```

Expected: PASS.

---

### Task 4: Rule-pack loading and precedence resolution

**Files:**
- Create: `src/masiv/rules.py`
- Test: `tests/test_rules.py`

- [ ] **Step 1: Write failing rule tests**

Create `tests/test_rules.py`:

```python
import json
from pathlib import Path

from masiv.models import EvidenceStrength
from masiv.rules import load_rule_pack, resolve_rule_packs


def test_load_rule_pack_from_json(tmp_path: Path) -> None:
    path = tmp_path / "base.json"
    path.write_text(
        json.dumps(
            {
                "name": "base_acmg_2015",
                "version": "2015",
                "precedence": 10,
                "criteria": {
                    "PM2": {
                        "criterion": "PM2",
                        "direction": "pathogenic",
                        "default_strength": "moderate",
                        "enabled": True,
                        "rule_version": "ACMG_2015",
                        "thresholds": {"max_af": 0.0001},
                        "citations": ["Richards 2015"],
                    }
                },
                "source_manifest": [
                    {"name": "ACMG/AMP", "version": "2015", "kind": "guideline"}
                ],
            }
        )
    )

    pack = load_rule_pack(path)

    assert pack.name == "base_acmg_2015"
    assert pack.criteria["PM2"].default_strength is EvidenceStrength.MODERATE
    assert pack.source_manifest[0].kind == "guideline"


def test_resolve_rule_packs_applies_precedence_and_records_override() -> None:
    base = load_rule_pack(
        {
            "name": "base_acmg_2015",
            "version": "2015",
            "precedence": 10,
            "criteria": {
                "PM2": {
                    "criterion": "PM2",
                    "direction": "pathogenic",
                    "default_strength": "moderate",
                    "enabled": True,
                    "rule_version": "ACMG_2015",
                    "thresholds": {"max_af": 0.0001},
                    "citations": ["Richards 2015"],
                }
            },
            "source_manifest": [
                {"name": "ACMG/AMP", "version": "2015", "kind": "guideline"}
            ],
        }
    )
    svi = load_rule_pack(
        {
            "name": "clingen_svi_generic",
            "version": "2020",
            "precedence": 20,
            "criteria": {
                "PM2": {
                    "criterion": "PM2",
                    "direction": "pathogenic",
                    "default_strength": "supporting",
                    "enabled": True,
                    "rule_version": "PM2_SVI_2020",
                    "thresholds": {"max_af": 0.0001},
                    "citations": ["ClinGen SVI PM2"],
                }
            },
            "source_manifest": [
                {"name": "ClinGen SVI", "version": "2020", "kind": "guideline"}
            ],
        }
    )

    resolution = resolve_rule_packs([svi, base])

    assert resolution.rule_packs == ["base_acmg_2015", "clingen_svi_generic"]
    assert resolution.active_rules["PM2"].default_strength is EvidenceStrength.SUPPORTING
    assert resolution.active_rules["PM2"].rule_version == "PM2_SVI_2020"
    assert len(resolution.overrides) == 3
    assert {override.field for override in resolution.overrides} == {
        "default_strength",
        "rule_version",
        "citations",
    }
    assert [entry.name for entry in resolution.source_manifest] == ["ACMG/AMP", "ClinGen SVI"]
```

- [ ] **Step 2: Run rule tests to verify they fail**

Run:

```bash
python -m pytest tests/test_rules.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'masiv.rules'`.

- [ ] **Step 3: Implement rule loading and resolution**

Create `src/masiv/rules.py`:

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from masiv.exceptions import RulePackError
from masiv.models import CriterionRule, OverriddenValue, RulePack, RuleResolution, SourceManifestEntry


def load_rule_pack(source: str | Path | dict[str, Any]) -> RulePack:
    if isinstance(source, dict):
        payload = source
    else:
        path = Path(source)
        try:
            payload = json.loads(path.read_text())
        except OSError as error:
            raise RulePackError(f"could not read rule pack {path}") from error
        except json.JSONDecodeError as error:
            raise RulePackError(f"rule pack {path} is not valid JSON") from error

    try:
        pack = RulePack.model_validate(payload)
    except ValidationError as error:
        raise RulePackError("rule pack does not match MASIV schema") from error

    normalized: dict[str, CriterionRule] = {}
    for criterion, rule in pack.criteria.items():
        normalized[criterion.upper()] = rule
    return pack.model_copy(update={"criteria": normalized})


def resolve_rule_packs(rule_packs: list[RulePack]) -> RuleResolution:
    ordered = sorted(rule_packs, key=lambda pack: pack.precedence)
    active_rules: dict[str, CriterionRule] = {}
    overrides: list[OverriddenValue] = []
    manifest: list[SourceManifestEntry] = []

    for pack in ordered:
        manifest.extend(pack.source_manifest)
        for criterion, new_rule in pack.criteria.items():
            old_rule = active_rules.get(criterion)
            if old_rule is not None:
                overrides.extend(_diff_rule(criterion, old_rule, new_rule, pack.name))
            active_rules[criterion] = new_rule

    return RuleResolution(
        active_rules=active_rules,
        rule_packs=[pack.name for pack in ordered],
        overrides=overrides,
        source_manifest=manifest,
    )


def _diff_rule(
    criterion: str,
    old_rule: CriterionRule,
    new_rule: CriterionRule,
    new_rule_pack: str,
) -> list[OverriddenValue]:
    old_payload = old_rule.model_dump(mode="json")
    new_payload = new_rule.model_dump(mode="json")
    changes: list[OverriddenValue] = []
    for field, new_value in new_payload.items():
        old_value = old_payload.get(field)
        if old_value != new_value:
            changes.append(
                OverriddenValue(
                    criterion=criterion,
                    field=field,
                    old_rule_pack=old_rule.rule_version,
                    old_value=old_value,
                    new_rule_pack=new_rule_pack,
                    new_value=new_value,
                )
            )
    return changes
```

- [ ] **Step 4: Run rule tests**

Run:

```bash
python -m pytest tests/test_rules.py -v
```

Expected: PASS.

---

### Task 5: Point scoring, ACMG categorical combiner, and conflict detection

**Files:**
- Create: `src/masiv/combiner.py`
- Test: `tests/test_combiner.py`

- [ ] **Step 1: Write failing combiner tests**

Create `tests/test_combiner.py`:

```python
from masiv.combiner import combine_criteria, score_points
from masiv.models import Classification, CriterionDirection, CriterionResult, CriterionStatus, EvidenceStrength


def criterion(
    code: str,
    direction: CriterionDirection,
    strength: EvidenceStrength,
    status: CriterionStatus = CriterionStatus.MET,
) -> CriterionResult:
    return CriterionResult(
        criterion=code,
        direction=direction,
        strength=strength,
        status=status,
        rule_pack="synthetic",
        rule_version="test",
    )


def test_point_scoring_supports_modified_strengths() -> None:
    results = [
        criterion("PVS1", CriterionDirection.PATHOGENIC, EvidenceStrength.STRONG),
        criterion("PM2", CriterionDirection.PATHOGENIC, EvidenceStrength.SUPPORTING),
        criterion("BS1", CriterionDirection.BENIGN, EvidenceStrength.STRONG),
        criterion("PS3", CriterionDirection.PATHOGENIC, EvidenceStrength.MODERATE, CriterionStatus.NOT_MET),
    ]

    assert score_points(results) == 1


def test_pathogenic_combination_from_very_strong_and_strong() -> None:
    result = combine_criteria(
        [
            criterion("PVS1", CriterionDirection.PATHOGENIC, EvidenceStrength.VERY_STRONG),
            criterion("PS1", CriterionDirection.PATHOGENIC, EvidenceStrength.STRONG),
        ]
    )

    assert result.classification is Classification.PATHOGENIC
    assert result.acmg_rule == "PVS1_VeryStrong+>=1_Strong"
    assert result.criteria_used == ["PVS1", "PS1"]
    assert result.point_total == 12


def test_likely_pathogenic_combination_from_strong_and_moderate() -> None:
    result = combine_criteria(
        [
            criterion("PS1", CriterionDirection.PATHOGENIC, EvidenceStrength.STRONG),
            criterion("PM2", CriterionDirection.PATHOGENIC, EvidenceStrength.MODERATE),
        ]
    )

    assert result.classification is Classification.LIKELY_PATHOGENIC
    assert result.acmg_rule == "1_Strong+1-2_Moderate"


def test_benign_ba1_stand_alone() -> None:
    result = combine_criteria(
        [criterion("BA1", CriterionDirection.BENIGN, EvidenceStrength.STAND_ALONE)]
    )

    assert result.classification is Classification.BENIGN
    assert result.acmg_rule == "BA1"
    assert result.point_total == -8


def test_likely_benign_from_strong_and_supporting() -> None:
    result = combine_criteria(
        [
            criterion("BS1", CriterionDirection.BENIGN, EvidenceStrength.STRONG),
            criterion("BP4", CriterionDirection.BENIGN, EvidenceStrength.SUPPORTING),
        ]
    )

    assert result.classification is Classification.LIKELY_BENIGN
    assert result.acmg_rule == "1_BenignStrong+1_BenignSupporting"


def test_not_assessed_and_withheld_are_preserved_but_not_scored() -> None:
    result = combine_criteria(
        [
            criterion("PP3", CriterionDirection.PATHOGENIC, EvidenceStrength.SUPPORTING),
            criterion("PS2", CriterionDirection.PATHOGENIC, EvidenceStrength.STRONG, CriterionStatus.NOT_ASSESSED),
            criterion("BP4", CriterionDirection.BENIGN, EvidenceStrength.SUPPORTING, CriterionStatus.WITHHELD),
        ]
    )

    assert result.classification is Classification.VUS
    assert result.criteria_used == ["PP3"]
    assert result.criteria_not_assessed == ["PS2"]
    assert result.criteria_withheld == ["BP4"]
    assert result.point_total == 1


def test_high_strength_conflict_returns_vus_with_conflict() -> None:
    result = combine_criteria(
        [
            criterion("PS1", CriterionDirection.PATHOGENIC, EvidenceStrength.STRONG),
            criterion("BS1", CriterionDirection.BENIGN, EvidenceStrength.STRONG),
        ]
    )

    assert result.classification is Classification.VUS
    assert result.acmg_rule == "conflict_review"
    assert result.conflicts == ["high_strength_pathogenic_and_benign_evidence"]
```

- [ ] **Step 2: Run combiner tests to verify they fail**

Run:

```bash
python -m pytest tests/test_combiner.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'masiv.combiner'`.

- [ ] **Step 3: Implement combiner**

Create `src/masiv/combiner.py`:

```python
from __future__ import annotations

from collections import Counter

from masiv.models import (
    Classification,
    ClassificationResult,
    CriterionDirection,
    CriterionResult,
    CriterionStatus,
    EvidenceStrength,
    SourceManifestEntry,
)

PATHOGENIC_POINTS = {
    EvidenceStrength.SUPPORTING: 1,
    EvidenceStrength.MODERATE: 2,
    EvidenceStrength.STRONG: 4,
    EvidenceStrength.VERY_STRONG: 8,
    EvidenceStrength.STAND_ALONE: 8,
}
BENIGN_POINTS = {
    EvidenceStrength.SUPPORTING: -1,
    EvidenceStrength.MODERATE: -2,
    EvidenceStrength.STRONG: -4,
    EvidenceStrength.VERY_STRONG: -8,
    EvidenceStrength.STAND_ALONE: -8,
}


def score_points(results: list[CriterionResult]) -> int:
    total = 0
    for result in results:
        if result.status is not CriterionStatus.MET:
            continue
        if result.direction is CriterionDirection.PATHOGENIC:
            total += PATHOGENIC_POINTS[result.strength]
        else:
            total += BENIGN_POINTS[result.strength]
    return total


def combine_criteria(
    results: list[CriterionResult],
    source_manifest: list[SourceManifestEntry] | None = None,
) -> ClassificationResult:
    met = [result for result in results if result.status is CriterionStatus.MET]
    withheld = [result.criterion for result in results if result.status is CriterionStatus.WITHHELD]
    not_assessed = [result.criterion for result in results if result.status is CriterionStatus.NOT_ASSESSED]
    point_total = score_points(results)
    conflicts = _detect_conflicts(met)

    if conflicts:
        return ClassificationResult(
            classification=Classification.VUS,
            acmg_rule="conflict_review",
            point_total=point_total,
            criteria_used=[result.criterion for result in met],
            criteria_withheld=withheld,
            criteria_not_assessed=not_assessed,
            conflicts=conflicts,
            source_manifest=source_manifest or [],
        )

    classification, rule = _classify_without_conflict(met)
    return ClassificationResult(
        classification=classification,
        acmg_rule=rule,
        point_total=point_total,
        criteria_used=[result.criterion for result in met],
        criteria_withheld=withheld,
        criteria_not_assessed=not_assessed,
        conflicts=[],
        source_manifest=source_manifest or [],
    )


def _detect_conflicts(met: list[CriterionResult]) -> list[str]:
    has_pathogenic_strong = any(
        result.direction is CriterionDirection.PATHOGENIC
        and result.strength in {EvidenceStrength.STRONG, EvidenceStrength.VERY_STRONG}
        for result in met
    )
    has_benign_strong = any(
        result.direction is CriterionDirection.BENIGN
        and result.strength in {EvidenceStrength.STRONG, EvidenceStrength.VERY_STRONG, EvidenceStrength.STAND_ALONE}
        for result in met
    )
    if has_pathogenic_strong and has_benign_strong:
        return ["high_strength_pathogenic_and_benign_evidence"]
    return []


def _classify_without_conflict(met: list[CriterionResult]) -> tuple[Classification, str]:
    pathogenic_counts = _count_strengths(met, CriterionDirection.PATHOGENIC)
    benign_counts = _count_strengths(met, CriterionDirection.BENIGN)

    if any(
        result.criterion == "BA1"
        and result.direction is CriterionDirection.BENIGN
        and result.strength is EvidenceStrength.STAND_ALONE
        for result in met
    ):
        return Classification.BENIGN, "BA1"

    if benign_counts[EvidenceStrength.STRONG] >= 2:
        return Classification.BENIGN, ">=2_BenignStrong"

    if _is_pathogenic(pathogenic_counts):
        return Classification.PATHOGENIC, _pathogenic_rule(pathogenic_counts)

    if _is_likely_pathogenic(pathogenic_counts):
        return Classification.LIKELY_PATHOGENIC, _likely_pathogenic_rule(pathogenic_counts)

    if (
        benign_counts[EvidenceStrength.STRONG] >= 1
        and benign_counts[EvidenceStrength.SUPPORTING] >= 1
    ):
        return Classification.LIKELY_BENIGN, "1_BenignStrong+1_BenignSupporting"

    if benign_counts[EvidenceStrength.SUPPORTING] >= 2:
        return Classification.LIKELY_BENIGN, ">=2_BenignSupporting"

    return Classification.VUS, "no_combination_met"


def _count_strengths(
    met: list[CriterionResult], direction: CriterionDirection
) -> Counter[EvidenceStrength]:
    return Counter(result.strength for result in met if result.direction is direction)


def _is_pathogenic(counts: Counter[EvidenceStrength]) -> bool:
    very_strong = counts[EvidenceStrength.VERY_STRONG]
    strong = counts[EvidenceStrength.STRONG]
    moderate = counts[EvidenceStrength.MODERATE]
    supporting = counts[EvidenceStrength.SUPPORTING]
    return (
        (very_strong >= 1 and strong >= 1)
        or (very_strong >= 1 and moderate >= 2)
        or (very_strong >= 1 and moderate >= 1 and supporting >= 1)
        or (very_strong >= 1 and supporting >= 2)
        or strong >= 2
        or (strong >= 1 and moderate >= 3)
        or (strong >= 1 and moderate >= 2 and supporting >= 2)
        or (moderate >= 3 and supporting >= 2)
    )


def _pathogenic_rule(counts: Counter[EvidenceStrength]) -> str:
    very_strong = counts[EvidenceStrength.VERY_STRONG]
    strong = counts[EvidenceStrength.STRONG]
    moderate = counts[EvidenceStrength.MODERATE]
    supporting = counts[EvidenceStrength.SUPPORTING]
    if very_strong >= 1 and strong >= 1:
        return "PVS1_VeryStrong+>=1_Strong"
    if very_strong >= 1 and moderate >= 2:
        return "PVS1_VeryStrong+>=2_Moderate"
    if very_strong >= 1 and moderate >= 1 and supporting >= 1:
        return "PVS1_VeryStrong+1_Moderate+1_Supporting"
    if very_strong >= 1 and supporting >= 2:
        return "PVS1_VeryStrong+>=2_Supporting"
    if strong >= 2:
        return ">=2_Strong"
    if strong >= 1 and moderate >= 3:
        return "1_Strong+>=3_Moderate"
    if strong >= 1 and moderate >= 2 and supporting >= 2:
        return "1_Strong+2_Moderate+>=2_Supporting"
    return ">=3_Moderate+>=2_Supporting"


def _is_likely_pathogenic(counts: Counter[EvidenceStrength]) -> bool:
    very_strong = counts[EvidenceStrength.VERY_STRONG]
    strong = counts[EvidenceStrength.STRONG]
    moderate = counts[EvidenceStrength.MODERATE]
    supporting = counts[EvidenceStrength.SUPPORTING]
    return (
        (very_strong >= 1 and moderate >= 1)
        or (very_strong >= 1 and supporting >= 1)
        or (strong >= 1 and 1 <= moderate <= 2)
        or (strong >= 1 and supporting >= 2)
        or moderate >= 3
        or (moderate >= 2 and supporting >= 2)
        or (moderate >= 1 and supporting >= 4)
    )


def _likely_pathogenic_rule(counts: Counter[EvidenceStrength]) -> str:
    very_strong = counts[EvidenceStrength.VERY_STRONG]
    strong = counts[EvidenceStrength.STRONG]
    moderate = counts[EvidenceStrength.MODERATE]
    supporting = counts[EvidenceStrength.SUPPORTING]
    if very_strong >= 1 and moderate >= 1:
        return "PVS1_VeryStrong+1_Moderate"
    if very_strong >= 1 and supporting >= 1:
        return "PVS1_VeryStrong+1_Supporting"
    if strong >= 1 and 1 <= moderate <= 2:
        return "1_Strong+1-2_Moderate"
    if strong >= 1 and supporting >= 2:
        return "1_Strong+>=2_Supporting"
    if moderate >= 3:
        return ">=3_Moderate"
    if moderate >= 2 and supporting >= 2:
        return "2_Moderate+>=2_Supporting"
    return "1_Moderate+>=4_Supporting"
```

- [ ] **Step 4: Run combiner tests**

Run:

```bash
python -m pytest tests/test_combiner.py -v
```

Expected: PASS.

---

### Task 6: Thin CLI for parse and combine workflows

**Files:**
- Create: `src/masiv/cli.py`
- Create: `tests/fixtures/criteria_likely_pathogenic.json`
- Test: `tests/test_cli.py`

- [ ] **Step 1: Create criteria fixture**

Create `tests/fixtures/criteria_likely_pathogenic.json`:

```json
{
  "criteria": [
    {
      "criterion": "PS1",
      "direction": "pathogenic",
      "strength": "strong",
      "status": "met",
      "rule_pack": "synthetic",
      "rule_version": "test"
    },
    {
      "criterion": "PM2",
      "direction": "pathogenic",
      "strength": "moderate",
      "status": "met",
      "rule_pack": "synthetic",
      "rule_version": "test"
    },
    {
      "criterion": "PS3",
      "direction": "pathogenic",
      "strength": "strong",
      "status": "not_assessed",
      "rule_pack": "synthetic",
      "rule_version": "test",
      "limitations": ["No functional assay evidence supplied."]
    }
  ],
  "source_manifest": [
    {"name": "synthetic", "version": "test", "kind": "fixture"}
  ]
}
```

- [ ] **Step 2: Write failing CLI tests**

Create `tests/test_cli.py`:

```python
import json
from pathlib import Path

from masiv.cli import main

FIXTURES = Path(__file__).parent / "fixtures"


def test_cli_parse_writes_normalized_variant_json(tmp_path: Path) -> None:
    output_path = tmp_path / "variants.json"

    exit_code = main(["parse", str(FIXTURES / "sample.vcf"), "--output", str(output_path)])

    assert exit_code == 0
    payload = json.loads(output_path.read_text())
    assert payload["header"]["genome_build"] == "GRCh38"
    assert payload["variants"][0]["chromosome"] == "1"
    assert payload["variants"][0]["samples"][0]["genotype"] == "0/1"


def test_cli_combine_writes_classification_json(tmp_path: Path) -> None:
    output_path = tmp_path / "classification.json"

    exit_code = main(
        ["combine", str(FIXTURES / "criteria_likely_pathogenic.json"), "--output", str(output_path)]
    )

    assert exit_code == 0
    payload = json.loads(output_path.read_text())
    assert payload["classification"] == "Likely Pathogenic"
    assert payload["acmg_rule"] == "1_Strong+1-2_Moderate"
    assert payload["criteria_not_assessed"] == ["PS3"]
    assert payload["source_manifest"][0]["name"] == "synthetic"
```

- [ ] **Step 3: Run CLI tests to verify they fail**

Run:

```bash
python -m pytest tests/test_cli.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'masiv.cli'`.

- [ ] **Step 4: Implement CLI**

Create `src/masiv/cli.py`:

```python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from pydantic import ValidationError

from masiv.combiner import combine_criteria
from masiv.exceptions import MasivError
from masiv.models import CriterionResult, SourceManifestEntry
from masiv.vcf import parse_vcf_file


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "parse":
            return _parse_command(args.input, args.output)
        if args.command == "combine":
            return _combine_command(args.input, args.output)
    except (MasivError, ValidationError, OSError, json.JSONDecodeError) as error:
        print(f"masiv: {error}", file=sys.stderr)
        return 2
    parser.print_help(sys.stderr)
    return 2


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="masiv")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parse_parser = subparsers.add_parser("parse", help="parse VCF into normalized JSON")
    parse_parser.add_argument("input", type=Path)
    parse_parser.add_argument("--output", "-o", type=Path, required=True)

    combine_parser = subparsers.add_parser("combine", help="combine criterion JSON into classification JSON")
    combine_parser.add_argument("input", type=Path)
    combine_parser.add_argument("--output", "-o", type=Path, required=True)

    return parser


def _parse_command(input_path: Path, output_path: Path) -> int:
    result = parse_vcf_file(input_path)
    output_path.write_text(result.model_dump_json(indent=2) + "\n")
    return 0


def _combine_command(input_path: Path, output_path: Path) -> int:
    payload = json.loads(input_path.read_text())
    criteria = [CriterionResult.model_validate(item) for item in payload.get("criteria", [])]
    manifest = [
        SourceManifestEntry.model_validate(item) for item in payload.get("source_manifest", [])
    ]
    result = combine_criteria(criteria, source_manifest=manifest)
    output_path.write_text(result.model_dump_json(indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Run CLI tests**

Run:

```bash
python -m pytest tests/test_cli.py -v
```

Expected: PASS.

- [ ] **Step 6: Run installed CLI smoke commands**

Run:

```bash
masiv parse /data/code/mavif/tests/fixtures/sample.vcf --output /tmp/masiv-variants.json
masiv combine /data/code/mavif/tests/fixtures/criteria_likely_pathogenic.json --output /tmp/masiv-classification.json
```

Expected: both commands exit with code 0 and write JSON output files.

---

### Task 7: Full verification and command documentation update

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Run the full test suite**

Run:

```bash
python -m pytest
```

Expected: PASS for all tests.

- [ ] **Step 2: Run Ruff**

Run:

```bash
python -m ruff check .
```

Expected: PASS with no lint violations.

- [ ] **Step 3: Run mypy**

Run:

```bash
python -m mypy src
```

Expected: PASS with no type errors.

- [ ] **Step 4: Run CLI smoke checks**

Run:

```bash
masiv parse /data/code/mavif/tests/fixtures/sample.vcf --output /tmp/masiv-variants.json
masiv combine /data/code/mavif/tests/fixtures/criteria_likely_pathogenic.json --output /tmp/masiv-classification.json
python -m json.tool /tmp/masiv-variants.json >/dev/null
python -m json.tool /tmp/masiv-classification.json >/dev/null
```

Expected: all commands exit with code 0.

- [ ] **Step 5: Update verified development commands in `CLAUDE.md`**

Replace the current unverified command section with:

```markdown
## Development commands

Verified Phase A commands:

```bash
python -m pytest
python -m pytest tests/path/test_file.py::test_name -v
python -m ruff check .
python -m ruff format .
python -m mypy src
masiv parse tests/fixtures/sample.vcf --output /tmp/masiv-variants.json
masiv combine tests/fixtures/criteria_likely_pathogenic.json --output /tmp/masiv-classification.json
```
```

- [ ] **Step 6: Re-run verification after documentation update**

Run:

```bash
python -m pytest
python -m ruff check .
python -m mypy src
```

Expected: all pass.

---

## Self-review notes

Spec coverage:

- Python package metadata: Task 1.
- Pydantic contracts: Task 2.
- VCF parsing to JSON-ready variants: Task 3.
- Rule-pack JSON loading and precedence: Task 4.
- ACMG categorical combiner, point scoring, modified strengths, conflict detection: Task 5.
- Thin CLI for parse/combine: Task 6.
- pytest, Ruff, mypy, verified commands, and `CLAUDE.md` update: Task 7.

Type consistency:

- Model names used by tests match `src/masiv/models.py` definitions.
- CLI imports `CriterionResult`, `SourceManifestEntry`, `combine_criteria`, and `parse_vcf_file`, all defined in earlier tasks.
- Combiner returns `ClassificationResult`, using enum values that serialize to the exact strings asserted by CLI tests.

Scope check:

- No Phase B clinical criteria engines are included.
- No annotation engine, ClinVar/ClinGen retrieval, PVS1 logic, or literature extraction is included.
- VCF remains the primary external input, and JSON remains the internal/final artifact format.
