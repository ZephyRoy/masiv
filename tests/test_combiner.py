from masiv.combiner import combine_criteria, score_points
from masiv.models import (
    Classification,
    CriterionDirection,
    CriterionResult,
    CriterionStatus,
    EvidenceStrength,
)


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
        criterion(
            "PS3",
            CriterionDirection.PATHOGENIC,
            EvidenceStrength.MODERATE,
            CriterionStatus.NOT_MET,
        ),
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
            criterion(
                "PS2",
                CriterionDirection.PATHOGENIC,
                EvidenceStrength.STRONG,
                CriterionStatus.NOT_ASSESSED,
            ),
            criterion(
                "BP4",
                CriterionDirection.BENIGN,
                EvidenceStrength.SUPPORTING,
                CriterionStatus.WITHHELD,
            ),
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
