# Phase A MASIV Core Design

## Purpose

Phase A establishes the deterministic foundation for MASIV: VCF-first input normalization, JSON-serializable contracts, rule-pack resolution, source manifests, and classification combiners. It does not implement clinical criterion engines such as BA1, PM2, or PVS1; it creates the structures those engines will use in later phases.

## Scope

Phase A includes:

- a Python package named `masiv`;
- Pydantic models for normalized variants, disease context, evidence records, criterion results, source manifests, rule packs, and final classifications;
- VCF or VCF-like parsing into normalized JSON-ready variant objects;
- JSON rule-pack loading and precedence resolution;
- ACMG/AMP 2015 categorical combination from already-computed criterion results;
- point-system scoring for signed evidence strengths;
- conflict detection for mixed pathogenic and benign evidence;
- a thin CLI for parsing VCF inputs and combining synthetic criteria JSON;
- pytest, Ruff, and mypy configuration with tests for the above behavior.

Phase A excludes:

- annotation execution with VEP, ANNOVAR, or SnpEff;
- population frequency criteria such as BA1, BS1, PM2, or BS2;
- PVS1 decision-tree logic;
- ClinVar/ClinGen retrieval;
- literature extraction or agentic criterion assignment.

## Architecture

The package will be split into small deterministic modules:

- `masiv.models`: shared Pydantic models and enums.
- `masiv.vcf`: VCF parsing and normalization into model objects.
- `masiv.rules`: rule-pack model loading and precedence resolution.
- `masiv.combiner`: ACMG categorical and point-system classification logic.
- `masiv.cli`: thin command-line entry points for parse/combine smoke workflows.

The CLI is intentionally thin. Core behavior lives in importable functions so tests can exercise deterministic logic directly.

## Data flow

1. A user provides a VCF or VCF-like file as the primary input.
2. `masiv.vcf` parses metadata, contigs, samples, INFO values, FORMAT keys, and per-sample genotype fields.
3. Each VCF record becomes a normalized `Variant` object that preserves source file, line number, genome build if present, coordinates, alleles, IDs, quality, filters, INFO, samples, genotype data, and optional disease/transcript context.
4. `Variant` objects serialize to JSON for downstream annotation, evidence retrieval, criterion engines, and reports.
5. Rule-pack JSON files define criteria metadata, strength overrides, thresholds, citations, source versions, and precedence.
6. `masiv.rules` resolves active rule packs in this order: `base_acmg_2015 -> clingen_svi_generic -> vcep_specific -> local_lab_policy_overrides`.
7. Criterion engines are represented in Phase A by synthetic `CriterionResult` inputs. The combiner uses these results to produce a deterministic `ClassificationResult`.
8. Final outputs are JSON artifacts. Any future Markdown or HTML report must be generated from JSON rather than maintained separately.

## Data contracts

Criterion results must preserve:

- criterion code;
- direction: pathogenic or benign;
- strength: supporting, moderate, strong, very strong, stand-alone, or modified strengths such as `PVS1_Strong` represented as criterion plus applied strength;
- status: `met`, `not_met`, `not_assessed`, or `withheld`;
- rule pack name and rule version;
- variant context: genome build, transcript, gene, disease, and inheritance when known;
- evidence records with source, version, field, raw value, threshold, accession or URL when safe, and notes;
- reasoning derived from structured evidence;
- limitations and missing inputs.

Final classifications must preserve:

- five-tier class: Pathogenic, Likely Pathogenic, VUS, Likely Benign, or Benign;
- ACMG categorical rule satisfied, if any;
- point total;
- criteria used;
- criteria withheld due to conflict or dependency;
- criteria not assessed;
- missing evidence;
- source/version manifest.

## Error handling

Phase A validates external boundaries and internal contracts. Malformed VCF structure, invalid rule-pack JSON, unsupported criterion codes, invalid strengths, invalid criterion statuses, or impossible combiner inputs should raise typed exceptions. The CLI should catch these exceptions and return clear non-zero failures.

Missing disease context, transcript context, annotation output, phenotype data, or evidence source data should not fail VCF parsing or classification combination. Missing context should be represented as optional fields, empty lists, `not_assessed` criteria, limitations, or missing-evidence entries depending on the output model.

## Testing strategy

Tests will be written before implementation for each core behavior:

- VCF parser handles metadata, one or more samples, INFO fields, FORMAT fields, filters, missing values, and multi-allelic records without losing provenance.
- Pydantic models serialize to JSON and deserialize without changing semantic values.
- Rule-pack resolution applies precedence and records overridden lower-priority values.
- Point scoring maps pathogenic supporting/moderate/strong/very-strong to +1/+2/+4/+8 and benign supporting/strong/stand-alone to negative scores suitable for internal consistency checks.
- ACMG categorical combiner handles synthetic examples for Pathogenic, Likely Pathogenic, VUS, Likely Benign, and Benign.
- Modified strengths such as PVS1 at Strong and PM2 at Supporting are supported.
- Conflicting high-strength pathogenic and benign evidence is flagged rather than silently averaged.
- CLI commands can parse a small VCF fixture and combine a synthetic criteria fixture.

## Tooling

The initial implementation will add Python project metadata with Pydantic, pytest, Ruff, and mypy. After verification, `CLAUDE.md` should be updated so the development commands are no longer marked as unverified.

## Success criteria

Phase A is complete when:

- package metadata exists;
- `python -m pytest` passes;
- `python -m ruff check .` passes;
- `python -m mypy src` passes;
- a sample VCF can be parsed into normalized JSON via CLI;
- a synthetic criteria JSON can be combined into a final classification JSON via CLI;
- the outputs preserve provenance, rule-pack information, point totals, conflicts, and not-assessed criteria.