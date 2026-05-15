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
