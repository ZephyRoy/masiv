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
                "source_manifest": [{"name": "ACMG/AMP", "version": "2015", "kind": "guideline"}],
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
            "source_manifest": [{"name": "ACMG/AMP", "version": "2015", "kind": "guideline"}],
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
            "source_manifest": [{"name": "ClinGen SVI", "version": "2020", "kind": "guideline"}],
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
