# Social Navigation Scenario Card Development Workflow
## STATUS: EDITED 2026-01-02
- SOURCE: Prompt to ChatGPT 5.2
- DRAFTED: ChatGPT 5.2, 2026-01-02
- EDITED: Anthony Francis centaur@logicalrobotics.com, 2026-01-02

## Overview

This document defines the **recommended workflow** for authoring, reviewing, and maintaining social navigation scenario cards in the `prosoc` project. The goal of this workflow is to ensure that scenario documents are:

- human-readable and reviewable,
- transparent about authorship and provenance,
- suitable for both human judgment and machine use,
- and appropriate for research and evaluation contexts.

This workflow is inspired by best practices from internet standards (e.g., RFCs), software requirements engineering, dataset/model cards, and emerging approaches to constitutional AI.


## Design Principles

The scenario workflow is guided by the following principles:

1. **Human and Machine Readbility**
   Scenarios should be easy to read and understand for both humans and machines,
   following the markdown with embedded YAML schema as used in the social navigation charter.

2. **Transparency over authority**  
   Scenarios should clearly state where they came from and how they were developed, rather than asserting correctness by fiat.

3. **Human accountability**  
   Machine-assisted drafts are welcome, but readiness for use must be explicitly attested by a human.

4. **Separation of concerns**  
   Authorship, review, and empirical validation are distinct stages and should not be conflated.

5. **Low friction**  
   The workflow should support rapid iteration and contribution without unnecessary bureaucracy.

6. **Future-proofing**  
   Provenance and status information should support later audits, studies, or revisions.


## Scenario Lifecycle

Each scenario progresses through a series of lifecycle states. Not all scenarios will reach all states.

### 1. SOURCE (optional)

Identifies prior material that inspired or informed the scenario. Examples might include:

- a section of a paper such as the Principles & Guidelines paper
- a previous version of this scenario or source for this variant
- a dataset, benchmark, or video collection
- a URL, DOI, or git commit

The SOURCE stage establishes the *lineage* of a scenario, not an endorsement of its content.

### 2. DRAFTED

The scenario has been articulated in concrete form, but may still be speculative, incomplete, or otherwise need revision. Draft characteristics include:

- may be machine-generated or human-authored
- may contain placeholders or rough language
- not yet suitable for evaluation use

Drafted scenarios are encouraged as a way to explore ideas and expand coverage.

### 3. EDITED

The scenario has been revised for clarity, consistency, and alignment with the conventions of the `prosoc` project. Editing typically includes:

- improving narrative clarity
- ensuring schema compliance
- aligning terminology with the charter
- removing ambiguity or contradictions

An EDITED scenario is structurally sound but not yet formally approved.

### 4. AUDITED

A human reviewer has examined the scenario and judged it ready for intended use. An audit asserts that the scenario:

- is internally coherent
- aligns with the Prosocial Navigation Charter
- reasonably captures a social navigation situation
- is suitable for use in evaluation, simulation, or analysis

Auditing does **not** imply empirical validation.

### 5. VALIDATED (optional)

The scenario has been supported by empirical evidence. Validation may include:

- user studies
- robot experiments
- simulation benchmarks
- inter-rater agreement analyses

VALIDATED scenarios should reference the supporting evidence.

### 6. DEPRECATED / RETIRED

The scenario is no longer recommended for use. Reasons may include:

- replacement by a newer version
- discovery of flaws or ambiguity
- changes in the charter or evaluation methodology

Deprecated scenarios should point to the preferred alternative when possible.


## Status Section Template

Each scenario document should include a concise STATUS section describing its current lifecycle state and provenance. Only fields that apply need to be included.

```markdown
## STATUS: EDITIED 2025-01-18
- SOURCE: P&G Paper, Section 4.2
- DRAFTED: ChatGPT (GPT-4.x), 2025-01-12
- EDITED: Anthony Francis centaur@logicalrobotics.com, 2025-01-18
```

More detailed versions may include AUDITED, VALIDATED, or DEPRECATED entries.

## Recommended Practices

- Human-readable content should be lightweight and easy to review.
- The `STATE` should be maintained so it is authoritative for readiness.
- Machine-generated content should not be assumed correct without review.
- Prefer checked-in incremental improvement over withholding until perfection.
- Scenario narratives should be human-readable; avoid over-specification.
- CI and schema validation should catch structural issues early.

## Relationship to Tooling

The `prosoc` project's tooling supports this workflow by:

- treating human-readable Markdown files as the source of truth
- extracting machine-readable YAML via a validated compiler
- enforcing consistency through schema-checking CI guardrails
- allowing safe iteration via dry-run and diff tools

This workflow is designed to complement the `prosoc` tooling, by providing clarity about the process, and is not designed for programmatic enforcement.

## Scope and Limitations

This workflow is for **research and development use**. We have not yet developed a formal safety certification process, sought regulatory approval, or worked through the issues needed for ethical endorsement. Real-world robotic deployment requires additional validation, testing, and oversight beyond the scope of this project.
