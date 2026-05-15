from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

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

    combine_parser = subparsers.add_parser(
        "combine", help="combine criterion JSON into classification JSON"
    )
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
