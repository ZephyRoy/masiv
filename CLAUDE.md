# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository status

This repository now contains the Phase A MASIV Python package scaffold, test suite, and build configuration. There is no README, Cursor rule, or Copilot instruction in the current tree. The project-specific guidance is this `CLAUDE.md` file and the material under `docs/`, especially `docs/acmg_automated_classification_research_report.md`.

## Project goal

MASIV is the Multi Agent System for Interpreting Variants. The current scope is automated germline sequence-variant ACMG/AMP classification, not full diagnosis, phenotype-driven prioritization, somatic interpretation, CNV scoring, or complete VCF-to-report clinical interpretation.

Stage 1 should build the framework and compute only deterministic ACMG criteria that can be calculated directly from structured annotations, databases, and hard-coded/versioned rules. VCF or VCF-like files are the primary external input format; JSON is used for normalized intermediate artifacts and final classification outputs. Agent/LLM components may orchestrate evidence retrieval and summarize structured outputs, but final criterion assignment and final classification must remain deterministic, auditable, and reproducible.

## Important source documents

Read these before designing or implementing ACMG logic:

- `docs/acmg_automated_classification_research_report.md` — primary project research report and stage-1 roadmap.
- `docs/papers/ACMG_guideline_2015_official.md` — ACMG/AMP 2015 base criteria and five-tier classification language.
- `docs/papers/autopvs1.md` — AutoPVS1 paper; use this for PVS1 design and integration decisions.
- `docs/papers/InterVar.md` — InterVar paper; useful for semi-automated ACMG criteria coverage and manual-adjustment boundaries.
- `docs/papers/point_system_ACMG.md` — point/Bayesian representation for internal consistency checks.
- `docs/papers/sherloc.md` and `docs/papers/autoACMG_thesis.md` — useful references for refined criteria, provenance, and comparison behavior.

## Development commands

Use the project-local virtual environment to avoid modifying system Python dependencies:

```bash
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e '.[dev]'
```

Verified Phase A commands:

```bash
.venv/bin/python -m pytest
.venv/bin/python -m pytest tests/path/test_file.py::test_name -v
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format .
.venv/bin/python -m ruff format --check .
.venv/bin/python -m mypy src
.venv/bin/masiv parse tests/fixtures/sample.vcf --output /tmp/masiv-variants.json
.venv/bin/masiv combine tests/fixtures/criteria_likely_pathogenic.json --output /tmp/masiv-classification.json
```

## Architecture direction

The framework should be evidence-first and rule-pack-driven:

1. Input layer accepts VCF or VCF-like files as the main external input. It should parse records into normalized JSON variant objects for downstream processing, preserving genome build, sample identifiers, INFO/FORMAT provenance, zygosity, genotype fields, and any supplied disease, family, phenotype, transcript, or source metadata.
2. Annotation layer runs or consumes VEP/ANNOVAR/SnpEff-style annotations and emits normalized variant/transcript/protein consequences. VEP is the preferred initial backbone to evaluate because it aligns well with modern Ensembl/MANE workflows and AutoPVS1-like logic; ANNOVAR remains relevant for InterVar compatibility and imported logic.
3. Context/rule-resolution layer chooses gene, disease, inheritance model, transcript policy, active rule pack, and rule precedence. Rule precedence should be: variant/transcript normalization, disease/gene context, VCEP-specific specification, ClinGen SVI generic recommendation, ACMG/AMP 2015 fallback, conservative local fallback.
4. Criterion engines compute one ACMG criterion or a tightly related criterion group. They return structured criterion results with status, strength, direction, evidence, rule version, limitations, and provenance; they should not return only booleans.
5. Evidence retrieval modules query or load population frequency, ClinVar/ClinGen, predictor, gene-disease, domain, and literature/functional evidence sources. Cache raw payloads and source versions.
6. Conflict/double-counting layer detects incompatible pathogenic/benign evidence and non-independent evidence sources before final classification.
7. Classification combiner deterministically applies ACMG/AMP 2015 combination rules and may also compute a point/Bayesian score for internal explanation and boundary analysis.
8. Report layer generates JSON first. Markdown/HTML reports should be derived from JSON, not maintained as separate source-of-truth outputs.

## Data model expectations

Criterion results should be JSON-serializable and provenance-rich. Preserve at least:

- criterion code, direction, strength, and status (`met`, `not_met`, `not_assessed`, `withheld`, or equivalent);
- active rule pack and rule version;
- normalized variant context: genome build, transcript, gene, disease, inheritance where available;
- evidence records with source, version, field, raw value, threshold, and accession/URL when safe and applicable;
- reasoning derived from structured evidence;
- limitations and missing inputs that could change classification.

Final classification objects should include the final five-tier class, ACMG combinatorial rule satisfied, optional point total, pathogenic and benign criteria used, criteria withheld due to dependency/conflict, criteria not assessed, missing evidence, and a source/version manifest.

## Stage-1 implementation plan

Phase A: rule and evidence foundation

- Define VCF parsing and normalization models plus JSON schemas or typed models for variants, disease context, evidence records, criterion results, source manifests, and final classification.
- Implement rule-pack loading/resolution with JSON/YAML threshold configuration and Python modules for algorithmic criteria.
- Implement the ACMG/AMP 2015 categorical combiner plus point-system scoring for signed evidence strengths.
- Add synthetic tests for modified strengths such as `PVS1_Strong`, `PM2_Supporting`, and conflict handling.

Phase B: deterministic high-automation criteria

- Implement BA1, BS1, PM2, and carefully constrained BS2 from gnomAD-style population frequency inputs. Use filtering allele frequency and ancestry-specific maximums where available; PM2 should default to Supporting per ClinGen SVI unless an active VCEP rule overrides it.
- Implement PP3, BP4, and BP7 using calibrated missense/splicing thresholds from the active rule pack. Do not score informal predictor voting as independent evidence.
- Implement PM4 and BP3 from consequence, protein length change, repeat-region, and domain annotations.
- Implement PS1 and PM5 from ClinVar/ClinGen expert-reviewed or high-review-status variant matches. Check disease match, transcript/protein representation, and mechanism before scoring.
- Implement PM1 only from VCEP-defined hotspots/domains initially; use generic domain logic only as an explicitly labeled fallback.
- Integrate AutoPVS1 or implement an AutoPVS1-like local PVS1 decision tree. PVS1 must consider transcript choice, NMD, splice rescue/cryptic splice effects, alternative start codons, affected exon/region importance, LoF disease mechanism, and VCEP overrides.

Phase C: evidence-centric output and validation

- Emit one JSON classification artifact per variant containing all met, not-met, withheld, and not-assessed criteria.
- Generate Markdown reports from JSON for human review.
- Build comparison harnesses against selected ClinGen expert examples, the AutoPVS1 56-variant benchmark for PVS1, InterVar-like outputs, AutoACMG examples, and high-review-status ClinVar variants.
- Track per-criterion precision/recall/not-assessable rates rather than relying only on final classification concordance.

Phase D: later agentic evidence extraction

- Add literature and functional-evidence assistance for PS3/BS3, PS4, PP1/BS4, and phenotype-specific PP4 only after deterministic core outputs are stable.
- Treat extracted paper evidence as candidate structured evidence requiring validation rules and human review; do not let free-text LLM judgments directly assign ACMG criteria.

## Criteria automation boundaries

Stage 1 should prefer these deterministic or mostly deterministic criteria: PVS1, BA1, BS1, PM2, PP3/BP4, BP7, PM4/BP3, PS1/PM5, and VCEP-defined PM1.

Leave these as structured-input or human-review criteria until appropriate inputs and validation rules exist: PS2, PS3, PS4, PM3, PM6, PP1, PP4, BS3, BS4, BP2, BP5.

Do not count PP5 or BP6 in final classification under current ClinGen SVI guidance. They can be used only as pointers to primary evidence.

## Reuse and integration guidance

- Evaluate direct reuse or wrapping of AutoPVS1 before reimplementing PVS1 from scratch.
- Use InterVar as a reference for coverage, annotation fields, and manual-adjustment boundaries, but do not copy outdated behavior blindly: PVS1 is too coarse, PM2 strength has changed under ClinGen SVI, and PP5/BP6 should not contribute to final scoring.
- Keep rule packs pluggable: `base_acmg_2015 -> clingen_svi_generic -> vcep_specific -> local_lab_policy_overrides`.
- Store thresholds, citations, and source versions with rule packs so classifications are reproducible.

## Design constraints

- VCF or VCF-like files are the primary user-facing input format; JSON is the internal interchange and final output format.
- Deterministic code owns clinical criterion assignment and final classification.
- Agentic/LLM components are for orchestration, retrieval, summarization, and candidate extraction from unstructured text.
- Every result must preserve provenance and explicitly distinguish `not_met`, `not_assessed`, and `withheld`.
- Prefer conservative behavior when context is missing: absence of disease context, transcript ambiguity, poor source review status, or unvalidated thresholds should reduce automation confidence rather than silently apply stronger evidence.
