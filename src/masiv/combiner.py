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
    not_assessed = [
        result.criterion for result in results if result.status is CriterionStatus.NOT_ASSESSED
    ]
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
        and result.strength
        in {EvidenceStrength.STRONG, EvidenceStrength.VERY_STRONG, EvidenceStrength.STAND_ALONE}
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
