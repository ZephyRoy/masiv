# MASIV

**Multi Agent System for Interpreting Variants**

MASIV is a research-oriented framework for automated germline sequence-variant interpretation under the ACMG/AMP classification system. Its goal is not to replace expert review, but to make the computable parts of variant classification more reproducible, auditable, and transparent.

The project treats classification as an evidence workflow rather than a black-box prediction problem. Variants enter through VCF or VCF-like files, are normalized into structured intermediate records, and are evaluated by deterministic rule engines that preserve the evidence, thresholds, rule versions, and limitations behind every criterion.

## What MASIV is building

- **VCF-first interpretation pipelines** for sequence variants and sample-level genotype context.
- **Deterministic ACMG/AMP criterion engines** for evidence that can be safely computed from structured annotations, databases, and versioned rules.
- **Rule-pack driven classification** that can incorporate ACMG/AMP 2015, ClinGen SVI recommendations, VCEP specifications, and local policy overlays.
- **Provenance-rich JSON outputs** that record what was used, what was withheld, what was not assessed, and what evidence is missing.
- **Agent-assisted evidence gathering** for future stages, while keeping final criterion assignment deterministic and inspectable.

## Current focus

MASIV is currently focused on the foundation for automated ACMG/AMP classification: VCF normalization, evidence models, rule-pack resolution, classification combiners, and testable JSON outputs. Later stages will expand toward high-automation criteria such as population frequency, computational prediction, prior variant knowledge, and carefully constrained PVS1 logic.

## Guiding principle

Clinical interpretation should be explainable at the level of evidence. MASIV is designed so every classification can answer: which criteria were applied, which rules were active, which sources were used, and what missing evidence could change the result.

MASIV is research software and should not be used as a substitute for qualified clinical genetics review.
