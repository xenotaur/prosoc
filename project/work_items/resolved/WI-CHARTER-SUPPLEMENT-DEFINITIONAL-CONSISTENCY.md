---
resolution: "Implemented and merged in PR #130 (commit fed0d17a05bc15e736fe15480be619ca19ebf93e) -- added the glossary's missing shared-environment-navigability branch to the Prosocial definition and corrected the baseline-vs-P9 distinction to match Principle 13's own Explanation (a reviewer finding caught and fixed an initial inversion of that distinction); moved P9 from emphasized to deprioritized in the high_urgency context, with the user's explicit confirmation, and corrected the P1/P9 prose attributing harm prevention to P1."
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-DEFINITIONAL-CONSISTENCY
title: "Reconcile the glossary definition of prosocial behavior and P9's emergency-context framing with the charter's formal definitions"
type: deliverable
status: resolved
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-PROOFREADING
depends_on: []
blocked_by: []
expected_actions: [edit_file, run_tests, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr, implement_lifecycle_state_change]
acceptance:
  - "The glossary definition of prosocial behavior includes both branches of the formal definition (improving another agent's navigation experience, and preserving/improving shared-environment navigability), while preserving the distinction that merely avoiding degradation is baseline, not P9"
  - "The high-urgency context's prose and machine-readable (YAML) representations of P9's role agree with each other and with the charter's definitions of P0, P1, P8, and P9"
  - "Harm prevention is attributed to P1 Safety (and P0 as applicable), not framed as P9's defining role"
required_evidence: [manual_review, test_output]
artifacts_expected:
  - src/prosoc/prnc/charter/charter.md
  - src/prosoc/prnc/contexts/high_urgency/context.md
---

## Summary
Two definitional-consistency gaps found by a second-pass external
proofread, both requiring a judgment call about the charter's actual
normative meaning rather than mechanical copyediting: the glossary
definition of "prosocial behavior" omits half of the formal definition,
and the high-urgency context's prose mischaracterizes P9's role relative
to P1 Safety.

## Problem / Context
Not independently re-verified page-by-page in this planning pass (unlike
the items in `WI-CHARTER-SUPPLEMENT-COPYEDIT-FIXES`); the executing
session should locate and confirm both passages in
`src/prosoc/prnc/charter/charter.md` before editing. As reported by the
proofread:

**Glossary vs. formal definition.** The charter's formal definition of
prosocial behavior (reported at "p. 2") has two branches: (1) improving
another agent's navigation experience, and (2) preserving or improving
the navigability of the shared environment. The glossary definition
(reported at "p. 11") describes only actions that improve the
experience/safety/success of others, omitting the shared-environment
branch. The fix needs to preserve the charter's existing distinction that
merely *avoiding* degradation of the shared environment is baseline
social behavior, while P9 (prosocial behavior) goes beyond that baseline
-- this is not a mechanical copy of one definition onto the other.

**P9 and harm prevention in emergency contexts.** The high-urgency
context's prose (reported at "p. 42") says "P9 (Prosocial Behavior) is
interpreted as prioritizing harm prevention over everyday politeness,"
but harm prevention is principally P1 Safety's role, not P9's -- P9 is
charter-defined as an optional, beyond-baseline principle. The
machine-readable specification (reported at "p. 43") also lists P9 as
"emphasized" in this context, which may or may not be the right
categorization once the prose is corrected -- the two representations
must end up making the same claim, whichever way it's resolved. The
reviewer's suggested direction: "P9 may be expressed through actions that
support others' emergency response or improve shared emergency
navigability, subject to P0, P1, and P8" -- offered as one possible
framing, not a mandated final wording.

### Duplication search
- In-repo: no existing work item covers charter glossary/definition
  consistency or per-context principle-emphasis framing.
- Recommendation: Proceed.

### Demand search
- Directly requested by the second-pass proofread (this session,
  2026-11-04).
- Recommendation: Proceed.

## Scope
Two specific, charter-content edits requiring semantic judgment, kept
separate from `WI-CHARTER-SUPPLEMENT-COPYEDIT-FIXES`'s mechanical fixes
precisely because they touch the charter's normative meaning and should
get the user's/author's review of the resulting wording before landing.

## Required Changes
1. Locate the formal definition of prosocial behavior and the glossary
   definition in `charter.md`; confirm the two-branch vs. one-branch gap
   described above against the actual current text.
2. Revise the glossary definition to include both branches, preserving
   the baseline-vs.-P9 distinction already established elsewhere in the
   charter.
3. Locate the high-urgency context's P9 prose and its machine-readable
   principle-emphasis list; confirm the harm-prevention mischaracterization
   against the actual current text.
4. Reconcile the prose with the charter's definitions of P0, P1, P8, and
   P9 -- attributing harm prevention correctly to P1 (and P0 where
   applicable) rather than P9 -- and decide, with grounding in the
   charter's own principle definitions, whether P9 should remain
   categorized as "emphasized" for this context. Ensure prose and
   machine-readable representation make the same claim.

## Non-Goals
- Does not change any principle's canonical definition in the charter's
  own principle sections (P0-P9) -- only the glossary's restatement and
  the high-urgency context's own framing of P9's role.
- Does not change any card's lifecycle state.

## Acceptance Criteria
- Glossary definition and formal definition agree on both branches.
- High-urgency context's prose and YAML agree with each other and with
  P0/P1/P8/P9's charter definitions.
- Golden file regenerated with human-reviewed diff.
- `scripts/test` / `lrh validate` pass.

## Validation
- `scripts/test`
- `lrh validate`
- Manual side-by-side comparison of the formal definition, glossary
  definition, and high-urgency context text in the regenerated PDF.

## Risk Notes
- These are judgment calls about the charter's actual normative content,
  not mechanical fixes -- the resulting wording should be confirmed with
  the user before landing, not auto-applied from the reviewer's suggested
  phrasing verbatim.

## Dependencies / Order
None. Independent of the other items in this workstream.
