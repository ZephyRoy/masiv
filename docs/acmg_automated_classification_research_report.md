# Research Report: Automated ACMG/AMP Classification for Stage-1 MASIV

Date: 2026-05-14

## 1. Scope

The near-term goal is an agentic framework for automated ACMG/AMP classification of sequence variants, starting from annotated or unannotated variants and producing:

- a five-tier class: Pathogenic, Likely Pathogenic, VUS, Likely Benign, or Benign;
- all criteria applied, not applied, or not assessable;
- strength and direction of each criterion;
- evidence and provenance for every assertion;
- a clear boundary between deterministic automation and evidence requiring curator review.

This report focuses on germline sequence-variant ACMG/AMP classification. It does not yet cover full diagnosis, phenotype-driven prioritization, somatic AMP/ASCO/CAP classification, CNV ACMG/ClinGen scoring, or complete VCF-to-report interpretation.

## 2. Sources Reviewed

### Local documents in `docs/papers/`

- `ACMG_guideline_2015_official.md` and `ACMG_guideline.md`: original ACMG/AMP 2015 sequence-variant guidelines.
- `InterVar.md`: InterVar paper and implementation details.
- `autopvs1.md`: AutoPVS1 paper and implementation details.
- `sherloc.md`: SHERLOC semiquantitative refinement of ACMG/AMP.
- `point_system_ACMG.md`: Bayesian/natural point-system translation of ACMG/AMP evidence strengths.
- `autoACMG_thesis.md`: AutoACMG thesis, including AutoACMG implementation, comparison with InterVar/GeneBe, and criteria-level performance table.

### External sources checked

- ACMG/AMP 2015 standard: Richards et al., "Standards and guidelines for the interpretation of sequence variants" ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4544753/)).
- ClinGen variant classification guidance index, including SVI recommendations and VCEP specifications ([ClinGen](https://clinicalgenome.org/tools/clingen-variant-classification-guidance/)).
- ClinGen PVS1 recommendation: Abou Tayoun et al. 2018 ([ClinGen](https://clinicalgenome.org/docs/recommendations-for-interpreting-the-loss-of-function-pvs1-acmg-amp-variant-criterion/)).
- ClinGen BA1 recommendation: Ghosh et al. 2018 ([ClinGen](https://clinicalgenome.org/docs/updated-recommendation-for-the-benign-stand-alone-acmg-amp-criterion/)).
- ClinGen reputable source criteria PP5/BP6 recommendation: Biesecker and Harrison 2018 ([ClinGen](https://clinicalgenome.org/docs/the-acmg-amp-reputable-source-criteria-for-the-interpretation-of-sequence-variants/)).
- ClinGen PM2 recommendation: SVI recommendation to use PM2 as Supporting by default ([ClinGen](https://clinicalgenome.org/docs/pm2-recommendation-for-absence-rarity/)).
- ClinGen functional evidence PS3/BS3 recommendation: Brnich et al. 2019 ([ClinGen](https://clinicalgenome.org/docs/recommendations-for-application-of-the-functional-evidence-ps3-bs3-criterion-using-the-acmg-amp-sequence-variant-interpretation/)).
- ClinGen computational evidence PP3/BP4 recommendation: Pejaver et al. 2022 ([ClinGen](https://clinicalgenome.org/docs/calibration-of-computational-tools-for-missense-variant-pathogenicity-classification-and-clingen-recommendations-for-pp3-bp4-cri/)).
- ClinGen splicing evidence recommendation: Walker et al. 2023 ([ClinGen](https://clinicalgenome.org/docs/application-of-the-acmg-amp-framework-to-capture-evidence-relevant-to-predicted-and-observed-impact-on-splicing-recommendations/)).
- ClinGen cSpec registry for disease/gene-specific ACMG/AMP specifications ([cSpec Registry](https://cspec.genome.network/cspec/ui/svi/)).
- InterVar: Li and Wang 2017 ([AJHG](https://www.cell.com/ajhg/fulltext/S0002-9297%2817%2930004-6), [GitHub](https://github.com/WGLab/InterVar)).
- AutoPVS1: Xiang et al. 2020 ([Hum Mutat DOI](https://doi.org/10.1002/humu.24051), [GitHub](https://github.com/JiguangPeng/autopvs1)).
- AutoACMG project documentation ([ReadTheDocs](https://auto-acmg.readthedocs.io/), [GitHub](https://github.com/bihealth/auto-acmg)).
- GeneBe ACMG automation: Stawinski and Ploski, Clinical Genetics 2024 ([PubMed](https://pubmed.ncbi.nlm.nih.gov/37757607/), [GeneBe](https://genebe.net/)).
- GenOtoScope: ACMG classification for congenital hearing loss variants ([PLOS Computational Biology](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009785)).
- BIAS-2015: automated ACMG classification tool published in Genome Medicine 2025 ([Genome Medicine](https://genomemedicine.biomedcentral.com/articles/10.1186/s13073-025-01581-y)).
- 2026 benchmark of phenotype-driven diagnostic tools, useful for later whole-pipeline expansion ([Bioinformatics](https://academic.oup.com/bioinformatics/article/42/2/btaf623/8483023)).

## 3. High-Level Findings

1. The current state of ACMG automation is not "fully automatic expert replacement." It is best understood as deterministic evidence gathering plus rule application, with explicit manual or curator checkpoints for evidence types that require clinical judgment, family data, functional assay validity, or literature interpretation.

2. The most successful tools automate only a subset of ACMG criteria. InterVar automates 18 of 28 criteria but requires manual adjustment for de novo, functional, phase/segregation, phenotype specificity, and alternative molecular basis criteria. AutoPVS1 deeply automates one criterion, PVS1, and performs much better than generic PVS1 rules because it follows ClinGen's refined PVS1 decision tree.

3. The field is moving from generic ACMG rules toward ClinGen SVI and VCEP-specified rules. A modern tool should treat ACMG 2015 as the base schema, then apply ClinGen SVI updates and gene/disease-specific VCEP overrides when available.

4. A reliable framework must be evidence-centric. For every criterion, it should store the raw evidence, database versions, transcript used, disease context, inheritance model, decision rule, and why the criterion was not used if it was withheld.

5. The best near-term "agentic" design is not an LLM assigning pathogenicity directly. It should be a supervisor orchestrating deterministic criterion engines, evidence retrieval agents, literature extraction agents, and validation checks. The final ACMG combiner should remain deterministic and auditable.

6. Criteria differ substantially in automability. Population frequency, consequence, computational prediction, same amino-acid change, and some domain/hotspot evidence are highly automatable. Functional assays, segregation, phenotype specificity, de novo confirmation, allelic phase, and case-control enrichment are only partially automatable unless structured case/lab data are provided.

## 4. Current Guideline Landscape

### 4.1 ACMG/AMP 2015 Base Framework

The original ACMG/AMP sequence-variant framework defines 28 evidence criteria:

- Pathogenic: PVS1, PS1-PS4, PM1-PM6, PP1-PP5.
- Benign: BA1, BS1-BS4, BP1-BP7.

Evidence is combined into five classes using qualitative strength combinations. This base guideline is still the common interchange language, but many phrases are underspecified for automation, such as "well-established functional studies," "mutational hot spot," "extremely low frequency," and "highly specific phenotype."

### 4.2 ClinGen SVI Updates

ClinGen SVI recommendations operationalize parts of ACMG/AMP. These are essential for a current implementation:

- PVS1 has variant-type and disease-mechanism decision trees and can be used at Very Strong, Strong, Moderate, Supporting, or not at all.
- BA1 has updated stand-alone use guidance and exceptions.
- PM2 is recommended at Supporting strength by default, not Moderate, unless disease/gene-specific guidance says otherwise.
- PP5 and BP6 are discouraged because reputable-source assertions without evidence should not be counted.
- PS3/BS3 require assay validation and calibration, ideally via odds of pathogenicity.
- PP3/BP4 should use calibrated computational predictors with defined thresholds, not informal voting across many tools.
- Splicing evidence is treated across multiple criteria, including PVS1, PS1, PP3/BP4, and BP7, depending on predicted or observed molecular consequence.
- De novo, segregation, and phenotype-specific criteria have more quantitative guidance than the original 2015 text.

### 4.3 VCEP-Specific Specifications

ClinGen Variant Curation Expert Panels publish disease/gene-specific criteria. These can override generic criteria:

- frequency thresholds differ by disease prevalence, penetrance, and inheritance;
- PVS1 may be downgraded or disallowed if LoF is not the disease mechanism;
- PM1 hotspot/domain rules may be defined for specific protein regions;
- PP3/BP4 predictor thresholds may be gene/disease-specific;
- PS3/BS3 assay validity may be specified for a disease domain.

A stage-1 system should therefore implement a rule resolution order:

1. Variant-type and transcript normalization.
2. Disease/gene context selection.
3. VCEP specification lookup from cSpec or internal curated configs.
4. ClinGen SVI generic recommendation.
5. ACMG/AMP 2015 fallback.
6. Tool-specific conservative fallback if no rule exists.

## 5. Review of Current Automation Methods

### 5.1 InterVar

InterVar was an early general-purpose semi-automated ACMG engine. It accepts pre-annotated variants or VCF files and can call ANNOVAR. It automatically scores 18 ACMG criteria:

`PVS1`, `PS1`, `PS4`, `PM1`, `PM2`, `PM4`, `PM5`, `PP2`, `PP3`, `PP5`, `BA1`, `BS1`, `BS2`, `BP1`, `BP3`, `BP4`, `BP6`, `BP7`.

It leaves these for manual input:

`PS2`, `PS3`, `PM3`, `PM6`, `PP1`, `PP4`, `BS3`, `BS4`, `BP2`, `BP5`.

Important implementation ideas from InterVar:

- Use annotation outputs plus internal databases to generate preliminary criteria.
- Separate automatic scoring from manual adjustment.
- Produce a criteria table, not just a class.
- Allow user-supplied evidence files to override or fill criteria.

Important limitations:

- Some rules are outdated relative to ClinGen SVI updates.
- PVS1 is too coarse compared with ClinGen's refined PVS1 decision tree.
- PP5/BP6 should not be counted under current ClinGen advice.
- Some thresholds are generic defaults and not disease-specific.
- The paper itself shows stronger concordance for benign classifications than pathogenic classifications, because pathogenic evidence often needs family, clinical, functional, or literature evidence.

### 5.2 AutoPVS1

AutoPVS1 is a narrow but deep implementation of ClinGen's PVS1 recommendation. It addresses:

- NMD prediction;
- biologically relevant transcript selection;
- importance of the truncated or altered region;
- exon clinical significance;
- cryptic or newly generated splice sites;
- alternative in-frame start codons;
- disease-mechanism adjustment;
- selected gene/disease-specific PVS1 rules.

In the local `autopvs1.md`, AutoPVS1 achieved 95% concordance with 56 ClinGen SVI-curated variants, while InterVar had much lower concordance for the same PVS1-specific benchmark. The major lesson is that high-quality automation often requires criterion-specific expert logic rather than one generic rule per ACMG criterion.

### 5.3 AutoACMG

AutoACMG is a newer open-source effort aimed at broader ACMG automation. The local thesis states that it integrates latest ClinGen updates, implements selected ACMG criteria, and compares against InterVar, AutoPVS1, VarSome, and GeneBe. Its appendix includes criteria-level outputs where each criterion has:

- name;
- prediction status;
- summary;
- description.

That output shape is close to what this project should adopt, but it should be strengthened with formal provenance, database versions, and rule versions.

The thesis also reports that AutoACMG still leaves some criteria as `NotAutomated`, including de novo, functional, segregation, phenotype-specific, phase, and alternative molecular basis criteria. This matches the broader field.

### 5.4 GeneBe

GeneBe implements automatic ACMG criteria assignment and reports validation against expert classifications. It is useful as a benchmark and as evidence that fully integrated web-based automated criteria assignment is feasible. Its reported strengths in the AutoACMG thesis table suggest strong performance for several criteria, especially when using updated data and rules. However, GeneBe is not a drop-in open-source engine for this project unless the available APIs and licenses fit the intended architecture.

### 5.5 BIAS-2015

BIAS-2015 is a 2025 Genome Medicine tool explicitly focused on automated ACMG classification and shows that the field is still actively refining rule-based automation. The key conceptual point is the same: a modern system should encode each criterion with explicit rules and support evidence traceability. It should be evaluated against expert-curated or ClinVar/ClinGen-derived benchmark sets, with attention to per-criterion performance rather than final-label accuracy alone.

### 5.6 Domain-Specific ACMG Tools

Examples include GenOtoScope for congenital hearing loss, VIP-HL for hearing loss, CardioClassifier/CardioVAI for cardiovascular genes, vaRHC for hereditary cancer genes, MAGI-ACMG, and cancer- or panel-specific tools. These tools matter because they show that disease-specific rule specialization often outperforms generic ACMG automation.

For MASIV stage 1, this argues for a pluggable rule-pack system:

- `base_acmg_2015`;
- `clingen_svi_generic`;
- `vcep_hearing_loss`;
- `vcep_cardiomyopathy`;
- `vcep_brca1_brca2`;
- future disease-specific packs.

### 5.7 SHERLOC and Point/Bayesian Systems

SHERLOC decomposes ambiguous ACMG criteria into many finer rules, assigns semiquantitative points, avoids double-counting related evidence, and treats clinical evidence as hierarchically stronger than functional prediction when they conflict.

Tavtigian et al.'s point system gives a Bayesian interpretation:

- pathogenic supporting = +1;
- pathogenic moderate = +2;
- pathogenic strong = +4;
- pathogenic very strong = +8;
- benign supporting = -1;
- benign strong = -4;
- benign very strong can be modeled as -8 even though the original ACMG framework does not explicitly define a benign very-strong category.

Approximate classification ranges:

- Pathogenic: >= 10 points;
- Likely Pathogenic: 6 to 9 points;
- VUS: 0 to 5 points or mixed unresolved evidence;
- Likely Benign: -1 to -6 points in the published point-system framing;
- Benign: <= -7 points.

For implementation, the 2015 ACMG combinatorial rules remain necessary for compatibility, but an internal point/Bayesian representation is useful for:

- comparing evidence strength across criteria;
- detecting double-counting;
- handling modified strengths such as PVS1_Strong or PM2_Supporting;
- explaining how close a variant is to a class boundary.

## 6. Criteria-by-Criteria Automation Map

Legend:

- High: mostly automatable from structured annotations/databases.
- Medium: automatable if structured case, family, disease, or curated-domain inputs exist.
- Low: requires literature extraction, assay evaluation, clinical interpretation, or human review.

| Criterion | Evidence question | Automation level | Current method pattern | Key pitfalls |
| --- | --- | --- | --- | --- |
| PVS1 | Predicted null variant in gene where LoF is a disease mechanism | High for variant mechanics, Medium for disease mechanism | Use AutoPVS1/ClinGen decision tree: transcript, consequence, NMD, exon importance, splice rescue/cryptic sites, alternative start codon, LoF mechanism | Wrong transcript, LoF not disease mechanism, exon skipping in-frame, disease-specific PVS1 overrides |
| PS1 | Same amino-acid change as known pathogenic variant | High with curated variant database | Match amino-acid substitution to ClinVar/ClinGen/LSDB P/LP variant; ensure existing variant evidence is valid; check whether mechanism may be splicing rather than protein change | Inheriting bad ClinVar assertions; same amino acid but different molecular mechanism; transcript mismatch |
| PS2 | Confirmed de novo in patient with disease and no family history | Medium if trio data provided | Use trio genotypes, parental confirmation, phenotype specificity, maternity/paternity confirmation, recurrence count | False de novo, mosaicism, weak phenotype match, missing parental identity confirmation |
| PS3 | Well-established functional study supports damaging effect | Low-Medium | Use ClinGen PS3/BS3 framework: assay validity, controls, replication, calibration to OddsPath; structured functional databases where available | Most functional papers are not calibrated; assay may not model disease mechanism |
| PS4 | Variant enriched in affected individuals vs controls | Medium-Low | Case-control OR/statistics or accumulated case observations; disease-matched cohorts | Population stratification, ascertainment, publication bias, phenotype heterogeneity |
| PM1 | Located in mutational hotspot or critical domain without benign variation | Medium-High | Use VCEP hotspot definitions, UniProt/InterPro domains, ClinVar P/LP and gnomAD benign depletion, domain-specific counts | Generic domain rules overcall; benign variation in same region; residue-level rather than domain-level mechanism |
| PM2 | Absent/rare in population databases | High | Query gnomAD frequency/FAF by ancestry, coverage, quality; apply SVI PM2_Supporting by default or VCEP threshold | Old ACMG used Moderate; frequency thresholds must consider disease prevalence, penetrance, inheritance |
| PM3 | Detected in trans with pathogenic variant for recessive disease | Medium if phase/cohort data exists | Use phased variants, parental genotypes, read-backed phasing, known P/LP second allele; apply point-based PM3 scaling | Phase unknown; second allele not truly P/LP; compound heterozygosity assumptions |
| PM4 | Protein length change from in-frame indel/stop-loss in non-repeat region | High | Consequence annotation, repeat-region annotation, protein length/domain context | Repetitive regions; small indels in tolerant loops; stop-loss effects vary |
| PM5 | Novel missense at residue where different missense is pathogenic | High-Medium | Match residue to known P/LP missense; ensure prior variant pathogenicity and missense mechanism | Residue has mixed benign/pathogenic variants; previous variant may affect splicing |
| PM6 | Assumed de novo without confirmed parental relationship | Medium if trio/case data exists | Same as PS2 but lower strength; use SVI de novo point system | Overuse from case reports; weak phenotype match |
| PP1 | Co-segregation with disease in family | Medium with pedigree data, otherwise Low | Use ClinGen PP1/BS4 guidance, informative meioses, LOD-like evidence, phenotype status | Incomplete penetrance, phenocopies, small families, uncertain affection status |
| PP2 | Missense variant in gene where missense is common disease mechanism and benign missense rare | Medium-High | Gene-level variant spectrum from ClinVar/ClinGen/VCEP; missense constraint and benign depletion | Circularity from ClinVar; gene may have multiple disease mechanisms |
| PP3 | Computational evidence supports deleterious effect | High for score retrieval, Medium for threshold validity | Use calibrated predictors and SVI thresholds; for missense, avoid informal voting; for splicing, use SpliceAI/MES with SVI splicing guidance | Multiple predictor consensus is not independent; thresholds are disease/gene-specific |
| PP4 | Phenotype/family history highly specific for gene disease | Medium with structured HPO and differential diagnosis, otherwise Low | HPO similarity, disease specificity, inheritance consistency, gene-disease validity | Phenotype-driven prioritization is not the same as ACMG evidence; circularity if candidate gene was chosen by phenotype |
| PP5 | Reputable source reports pathogenic without evidence | Deprecated/avoid | Do not count under current SVI recommendation; use source to find primary evidence instead | Double-counting and opaque assertions |
| BA1 | Allele frequency too high for disorder | High | gnomAD FAF/max AF and BA1 threshold, default 5% unless VCEP exceptions | Founder alleles, low-penetrance alleles, disease-specific thresholds |
| BS1 | Allele frequency greater than expected for disorder | High-Medium | Calculate maximum credible allele frequency from prevalence, penetrance, allelic/genetic heterogeneity, inheritance; use VCEP threshold where available | Bad prevalence/penetrance assumptions; ancestry-specific frequency |
| BS2 | Observed in healthy adult inconsistent with disease model | Medium | Homozygotes/heterozygotes in gnomAD or internal unaffected cohorts; age/penetrance model | Adult-onset, reduced penetrance, undiagnosed controls |
| BS3 | Functional study shows no damaging effect | Low-Medium | Same PS3/BS3 assay validation framework | Assay may not capture all disease mechanisms; negative assay may be weak evidence |
| BS4 | Lack of segregation in affected family members | Medium with pedigree data | ClinGen PP1/BS4 guidance; evaluate phenotype, penetrance, family structure | Phenocopies, misdiagnosis, non-paternity, locus heterogeneity |
| BP1 | Missense variant in gene where only truncating variants cause disease | Medium-High | Gene-level mechanism: LoF/truncating disease mechanism with missense tolerance | Genes with both LoF and missense disease mechanisms |
| BP2 | Variant observed in trans with pathogenic dominant variant or in cis with pathogenic variant | Medium | Phase and co-occurrence analysis; disease/inheritance context | Requires reliable phase and interpretation of other variant |
| BP3 | In-frame indel in repetitive region without known function | High-Medium | Consequence + repeat/low-complexity + domain annotation | Repeat annotation alone can be insufficient |
| BP4 | Computational evidence supports no effect | High for score retrieval, Medium for threshold validity | Calibrated benign thresholds for missense/splicing; no informal voting | Absence of predicted damage is not always benign |
| BP5 | Alternate molecular basis for disease | Low-Medium | Detect another P/LP variant explaining phenotype; evaluate gene-disease fit | Can be invalid for multilocus disease, blended phenotypes, recessive carriers |
| BP6 | Reputable source reports benign without evidence | Deprecated/avoid | Do not count; use source to find evidence | Opaque assertions and double-counting |
| BP7 | Synonymous variant with no predicted splice impact and low conservation | High-Medium | Consequence, splice prediction, distance to splice sites, conservation; use SVI splicing guidance | Deep intronic/regulatory effects; transcript-specific splice context |

## 7. Evidence and Data Sources Needed

### 7.1 Variant Normalization and Annotation

Required:

- genome build: GRCh37 and GRCh38 support;
- normalized VCF representation;
- HGVS genomic/coding/protein notation;
- transcript selection, preferably MANE Select / MANE Plus Clinical, with fallback to RefSeq/Ensembl;
- consequence annotation from VEP, ANNOVAR, SnpEff, or a comparable engine;
- splice-region and protein consequence annotation.

Recommended:

- GA4GH VRS identifiers for stable cross-resource variant identity;
- transcript-versioned HGVS strings;
- liftOver/cross-build mapping only when necessary and explicitly logged.

### 7.2 Population Frequency

Core:

- gnomAD genomes/exomes with ancestry-specific AF and FAF;
- coverage and quality flags;
- homozygote/hemizygote counts;
- internal lab controls if available.

Rules supported:

- BA1;
- BS1;
- BS2;
- PM2;
- some PVS1 disease-mechanism/exon significance checks.

### 7.3 Clinical Variant Databases

Core:

- ClinVar, including review status, submitter conflicts, condition, assertion date, and evidence availability;
- ClinGen Evidence Repository / VCEP expert assertions where available;
- locus-specific databases when licensed and clinically accepted;
- HGMD only if license permits and with caution because database pathogenic labels are not equivalent to evidence.

Rules supported:

- PS1;
- PM1;
- PM5;
- PP2/BP1;
- PVS1 exon/domain importance;
- evidence discovery for PS3/BS3, PP1/BS4, PS4, and disease-specific logic.

### 7.4 Gene-Disease and Disease Metadata

Core:

- ClinGen Gene-Disease Validity;
- OMIM disease inheritance and gene-phenotype relationships, subject to license constraints;
- MONDO/Orphanet disease identifiers;
- HPO phenotype ontology;
- disease prevalence, penetrance, allelic heterogeneity, and genetic heterogeneity estimates.

Rules supported:

- PVS1 disease mechanism;
- BA1/BS1 frequency thresholds;
- PP4 phenotype specificity;
- BP5 alternate molecular basis;
- PS2/PM6 phenotype consistency;
- VCEP selection.

### 7.5 Functional and Literature Evidence

Core:

- PubMed/PMC full text where available;
- MaveDB and other multiplex assay repositories;
- ClinGen VCEP-curated assay validity documents;
- variant-specific functional papers;
- structured extracted evidence with quotes, assay type, model system, controls, readout, calibration, and disease relevance.

Rules supported:

- PS3;
- BS3;
- PS4 in some cases;
- PP1/BS4 if pedigrees are published;
- PP4 if phenotype details are published.

### 7.6 Predictive Scores

Missense:

- REVEL, BayesDel, VEST4, MutPred2, AlphaMissense, ESM-based scores, CADD as supporting context.

Splicing:

- SpliceAI;
- MaxEntScan;
- dbscSNV where still used;
- transcript-aware splice annotations.

Constraint/context:

- LOEUF/pLI;
- regional missense constraint;
- domain annotations from UniProt, InterPro, Pfam;
- conservation scores.

Important principle: PP3/BP4 should not be assigned by "many tools agree" unless the chosen rule pack explicitly validates that approach. Modern SVI guidance favors calibrated thresholds.

## 8. Recommended Stage-1 Architecture

### 8.1 Core Design

Use an evidence-first, rule-pack-driven agentic framework:

1. Input Agent
   - Accept VCF, HGVS, or normalized variant object.
   - Capture disease/gene context if provided.
   - Validate genome build, sample identifiers, zygosity, family structure, and phenotype fields.

2. Annotation Agent
   - Run or consume VEP/ANNOVAR/SnpEff annotations.
   - Normalize transcript and protein consequences.
   - Produce canonical variant representation.

3. Context Agent
   - Resolve gene, disease, inheritance, transcript, VCEP rule pack, and ClinGen gene-disease validity.
   - Select rule precedence.

4. Criterion Agents
   - One micro-agent per ACMG criterion or tightly related criterion group.
   - Deterministic code wherever possible.
   - Each returns structured evidence objects, not only boolean results.

5. Evidence Retrieval Agents
   - Query population, ClinVar/ClinGen, prediction, gene-disease, and literature resources.
   - Cache source versions and raw payloads.

6. Literature/Functional Agent
   - Use LLMs cautiously for evidence extraction from papers.
   - Output claims with exact citation, assay details, and uncertainty.
   - Never allow extracted text to become PS3/BS3 without validation rules.

7. Conflict and Double-Counting Agent
   - Detect contradictory pathogenic/benign evidence.
   - Detect non-independent evidence, such as PP3 and PS3 from the same functional mechanism or ClinVar-derived PS1 and PP5.
   - Apply rule-pack exclusions.

8. Classification Combiner
   - Apply ACMG/AMP 2015 combinations and optional point/Bayesian score.
   - Support modified strengths such as PVS1_Strong, PM2_Supporting, PS3_Moderate.
   - Preserve both final class and evidence path.

9. Explanation Agent
   - Generate human-readable explanation from structured evidence.
   - Include "not assessed" and "not used" criteria with reasons.

### 8.2 Data Model

A criterion result should look conceptually like:

```json
{
  "criterion": "PM2",
  "direction": "pathogenic",
  "strength": "supporting",
  "status": "met",
  "rule_pack": "clingen_svi_generic",
  "rule_version": "PM2_SVI_2020",
  "variant_context": {
    "genome_build": "GRCh38",
    "transcript": "NM_...",
    "gene": "GENE",
    "disease": "MONDO:..."
  },
  "evidence": [
    {
      "source": "gnomAD",
      "version": "v4.x",
      "field": "max_faf95",
      "value": 0.000001,
      "threshold": "below disease-specific PM2 threshold",
      "url_or_accession": "..."
    }
  ],
  "reasoning": "Variant is absent/rare in population data with adequate coverage; PM2 is applied at Supporting strength per ClinGen SVI.",
  "limitations": ["Disease-specific threshold unavailable; generic SVI fallback used."]
}
```

The final classification object should include:

- final class;
- ACMG combinatorial rule satisfied;
- optional point total and posterior estimate if implemented;
- pathogenic criteria used;
- benign criteria used;
- criteria withheld due to dependency or conflict;
- missing evidence that could change the class;
- source/version manifest.

### 8.3 Rule-Pack Strategy

Each criterion should be implemented as a rule module with:

- input schema;
- required evidence sources;
- output schema;
- strength levels supported;
- dependency/exclusion rules;
- test fixtures;
- source/guideline citation.

Rule packs should be composable:

```text
base_acmg_2015
  -> clingen_svi_generic
    -> vcep_specific_rule_pack
      -> local_lab_policy_overrides
```

When rule packs disagree, the output should show the active rule and the superseded rule.

## 9. Practical MVP Scope

For the first implementation, prioritize criteria with high automability and high impact:

### MVP-1: Deterministic Criteria

- PVS1 via an AutoPVS1-like implementation or direct integration.
- BA1, BS1, PM2 from gnomAD frequency and disease-specific thresholds.
- PP3/BP4 from calibrated missense/splicing predictors.
- BP7 for synonymous variants with no splice impact.
- PM4/BP3 for in-frame indels and repeat-region logic.
- PS1/PM5 from ClinVar/ClinGen expert-reviewed variant matching.
- PM1 from VCEP-defined hotspots/domains first; generic domain logic only as fallback.

### MVP-2: Semi-Automated Criteria with Structured Inputs

- PS2/PM6 if trio data and phenotype specificity are supplied.
- PM3/BP2 if phase or parental genotype data are supplied.
- PP1/BS4 if pedigree segregation observations are supplied.
- PP4 if HPO terms and disease specificity model are supplied.
- BS2 if unaffected cohort observations are supplied.
- BP5 if an alternate molecular diagnosis is supplied or detected in the same case.

### MVP-3: Literature/Functional Evidence Assistance

- PS3/BS3 evidence extraction from papers and assay databases.
- PS4 case-control evidence extraction.
- Human-review queue for extracted assertions.

This phasing avoids overclaiming automation while still producing useful ACMG classes for many variants.

## 10. Specific Implementation Notes by Criterion Group

### 10.1 Population Criteria: BA1, BS1, PM2, BS2

Population evidence should be implemented early because it is structured and often decisive.

Implementation details:

- Use gnomAD AF and filtering allele frequency rather than raw global AF alone.
- Use ancestry-specific maximum frequency.
- Check coverage and quality at the site before treating absence as evidence.
- Implement BA1 as stand-alone benign only when no exception applies.
- Implement BS1 using disease-specific max credible allele frequency:
  - prevalence;
  - penetrance;
  - inheritance;
  - allelic heterogeneity;
  - genetic heterogeneity.
- Implement PM2 as Supporting by default under ClinGen SVI.
- Implement BS2 only when population observation is truly inconsistent with disease model, age of onset, penetrance, and zygosity.

Agent role:

- compute thresholds;
- retrieve frequencies;
- explain threshold assumptions;
- flag missing disease prevalence/penetrance as a limitation.

### 10.2 Loss-of-Function Criterion: PVS1

PVS1 should not be a simple consequence check. It should follow ClinGen's two-stage logic:

1. Variant-specific effect:
   - nonsense/frameshift;
   - canonical splice;
   - initiation codon;
   - exon-level deletion/duplication;
   - NMD predicted or escaped;
   - truncation removes critical region;
   - exon skipping frameshift or in-frame;
   - cryptic splice rescue;
   - alternative start codon.

2. Disease mechanism:
   - LoF is known mechanism for selected gene-disease pair;
   - sufficient gene-disease validity;
   - gene/disease-specific VCEP overrides.

Recommended approach:

- evaluate whether AutoPVS1 can be integrated directly;
- otherwise implement its decision tree as a local module;
- add transcript-selection transparency;
- include VCEP-specific PVS1 overrides.

### 10.3 Computational Criteria: PP3, BP4, BP7, Splicing

Computational evidence should use calibrated thresholds.

Implementation details:

- Use separate predictors and thresholds for missense and splicing.
- Avoid counting many correlated predictors as independent evidence.
- For missense PP3/BP4, follow ClinGen's calibrated predictor recommendation when possible.
- For splicing:
  - predicted splice impact may support PP3;
  - lack of splice impact may support BP4 or BP7 depending on variant type;
  - observed RNA evidence can shift evidence into stronger criteria such as PVS1 or PS3/BS3, depending on consequence and assay quality.

Agent role:

- retrieve scores;
- select correct threshold from active rule pack;
- state why PP3/BP4/BP7 is or is not applied.

### 10.4 Prior Variant Knowledge: PS1, PM5, PM1, PP2, BP1

These depend heavily on curated clinical variant databases.

Implementation details:

- Prefer ClinGen expert panel and ClinVar high-review-status assertions.
- Do not blindly trust single-submit ClinVar P/LP assertions.
- Check disease match, transcript match, and molecular mechanism.
- For PS1, verify same amino-acid change and no different splice mechanism.
- For PM5, verify different pathogenic missense at same residue and avoid overuse if residue also has benign changes.
- For PP2/BP1, compute or load gene-level disease mechanism profiles.
- For PM1, prefer VCEP-defined hotspots over generic domain counting.

Agent role:

- build evidence graph around residue/domain/gene;
- identify contradictory benign evidence;
- flag when source evidence is opaque.

### 10.5 Case-Level Criteria: PS2, PM6, PM3, BP2, PP1, BS4, PP4, BP5

These criteria should be designed as structured-input first, literature-extraction second.

Implementation details:

- Define case data schema:
  - proband affected status;
  - HPO phenotypes;
  - family genotypes;
  - parental confirmation;
  - zygosity;
  - phase;
  - alternate diagnoses;
  - age/penetrance information.
- Use SVI point frameworks where available.
- Mark criterion as `not_assessed` if required case data are absent.
- Never infer de novo, segregation, or phase from a single-sample VCF.

Agent role:

- reason over pedigree and genotype structure;
- extract candidate case reports from literature;
- present evidence for curator validation.

### 10.6 Functional Criteria: PS3, BS3

Functional criteria are high-value but hard to automate safely.

Implementation details:

- Use ClinGen PS3/BS3 four-part approach:
  - define disease mechanism;
  - evaluate assay applicability;
  - evaluate controls and validation;
  - assign strength based on calibrated evidence.
- Use VCEP-approved assays when available.
- Treat high-throughput functional assays as structured evidence only if calibrated against known benign/pathogenic controls.
- Avoid using a functional claim from an abstract without assay details.

Agent role:

- retrieve papers;
- extract assay details, controls, variants, readouts, and conclusions;
- map assay to disease mechanism;
- score evidence quality for human review.

## 11. Classification Combiner

The framework should support two parallel views:

1. ACMG/AMP 2015 categorical combination rules.
2. Point/Bayesian representation for internal consistency checks and explanation.

The categorical rules are required for compatibility with clinical reporting. The point system is useful because ClinGen updates introduce modified strengths that are awkward in the original combinatorial table.

Implementation recommendation:

- store every criterion as a signed strength;
- compute both categorical and point totals;
- detect conflicts before final class;
- if strong benign and strong pathogenic evidence coexist, flag conflict rather than silently summing to VUS;
- log double-counting exclusions.

Conflict policy should be configurable but conservative:

- BA1 generally forces Benign unless an exception or rule-pack override applies.
- Contradictory high-strength evidence should trigger review.
- Deprecated PP5/BP6 should not affect final class.
- Evidence derived from the same source or same biological observation should not be double-counted.

## 12. Validation Strategy

A serious ACMG automation framework should be validated at three levels.

### 12.1 Per-Criterion Validation

Use benchmark datasets for each criterion:

- PVS1: ClinGen SVI curated PVS1 variants and AutoPVS1 benchmark cases.
- PP3/BP4: ClinGen calibrated predictor datasets.
- BA1/BS1/PM2: VCEP-curated frequency thresholds and expert-classified variants.
- PS3/BS3: VCEP assay-calibrated variants.
- PM3/PP1/de novo: ClinGen examples and VCEP curation examples.

Report precision, recall, false positives, false negatives, and "not assessable" rate per criterion.

### 12.2 Final Classification Validation

Compare final labels against:

- ClinGen expert panel classifications;
- ClinVar variants with high review status and no conflicts;
- VCEP-specific benchmark sets;
- internal manually curated cases if available.

Avoid overusing general ClinVar as ground truth because many ClinVar records are conflicting, old, single-submitter, or insufficiently evidenced.

### 12.3 Explanation Validation

For each variant, the output should answer:

- Which criteria changed the final class?
- Which evidence source supports each criterion?
- Which database versions were used?
- Which criteria were impossible to assess and why?
- What missing evidence would most likely move the variant out of VUS?

This is especially important for an agentic system because the output must be auditable.

## 13. Recommended Stage-1 Roadmap

### Phase A: Rule and Evidence Foundation

- Define variant, disease, evidence, criterion, and classification schemas.
- Implement source-version manifest.
- Implement ACMG 2015 combiner and point-system combiner.
- Implement rule-pack resolution.
- Add unit tests from synthetic examples.

### Phase B: High-Automation Criteria

- Integrate annotation engine.
- Implement BA1, BS1, PM2, BS2.
- Implement PP3, BP4, BP7.
- Implement PM4, BP3.
- Implement PS1, PM5.
- Implement PVS1 through AutoPVS1 integration or local implementation.

### Phase C: Evidence-Centric Output

- Produce JSON and Markdown reports per variant.
- Include per-criterion status and provenance.
- Include not-assessed criteria and required missing inputs.
- Build comparison harness against InterVar, GeneBe, AutoACMG, and selected ClinGen examples.

### Phase D: Agentic Evidence Extraction

- Add literature retrieval and extraction for PS3/BS3, PS4, PP1/BS4.
- Add phenotype matching for PP4.
- Keep human review for low-automation criteria.

## 14. Main Design Insight for MASIV

The agentic framework should treat ACMG classification as a set of auditable evidence transactions, not as a text-generation problem. LLM/agent components are valuable for orchestration, retrieval, summarization, and converting unstructured papers into candidate structured evidence. The final clinical classification should be produced by versioned deterministic rules that can be tested, reproduced, and inspected.

The best initial differentiator for MASIV would be:

- current ClinGen/VCEP-aware rule packs;
- per-criterion specialized agents;
- complete evidence provenance;
- explicit uncertainty and missing-evidence reporting;
- conservative treatment of non-automatable criteria;
- pluggable integration with existing tools such as AutoPVS1 rather than reimplementing everything at once.

## 15. Immediate Next Technical Decisions

1. Choose annotation backbone:
   - VEP is attractive because AutoPVS1 and many modern resources use Ensembl-style annotations.
   - ANNOVAR is convenient for InterVar compatibility but has licensing and update considerations.

2. Choose transcript policy:
   - Prefer MANE Select / MANE Plus Clinical.
   - Preserve all transcript consequences and show when classification depends on transcript choice.

3. Choose rule-pack format:
   - YAML/JSON for thresholds and citations.
   - Python modules for algorithmic criteria such as PVS1 and PM3.

4. Choose initial validation set:
   - ClinGen expert panel variants first.
   - AutoPVS1 56-variant set for PVS1.
   - ClinVar high-review-status variants only as secondary validation.

5. Choose output contract:
   - machine-readable JSON first;
   - Markdown/HTML report generated from JSON;
   - every criterion with evidence list and source manifest.

## 16. Bottom Line

Automated ACMG classification is feasible for a substantial subset of evidence, but full automation is unsafe if it hides missing or judgment-heavy criteria. Current best practice is a hybrid: deterministic criteria engines, guideline/version-aware rule packs, structured evidence provenance, and agentic assistance for evidence discovery and extraction. For stage 1, MASIV should build an ACMG classification core that is conservative, testable, and ClinGen/VCEP-aware, with room to add phenotype-driven filtering and prioritization later.
