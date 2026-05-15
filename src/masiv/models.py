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
