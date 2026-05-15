from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from masiv.exceptions import RulePackError
from masiv.models import (
    CriterionRule,
    OverriddenValue,
    RulePack,
    RuleResolution,
    SourceManifestEntry,
)


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
