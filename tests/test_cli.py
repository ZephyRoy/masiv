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
