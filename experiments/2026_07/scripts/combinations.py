"""
Curated (task, context, scenario) combinations for the 2026_07 packet
combinatorics experiment.

This is the single source of truth for both build_manifests.py (which turns
each entry into an ad-hoc packet manifest) and assemble_all.py (which
assembles each manifest and builds the comparison summary). Combinations are
hand-curated, not generated: prosoc has no scenario->task/context reference
edges (a deliberate deferral in PROP-NORMATIVE-PACKET-ASSEMBLY, Decision 3),
so pairing is a human judgment call grounded in each card's own role
description, not something the tooling can infer.

Each (task, context) pair below was picked for role coherence between the
task card's stated role and the context card's "Primary Role of Robot"
field; each scenario was picked for plausibility under that role plus
principle overlap with the task/context. See the pair-level "rationale"
field for the specific justification.
"""

from __future__ import annotations

from dataclasses import dataclass

CONSTITUTION = "asimov_three_laws"
JUSTIFICATION = "experiments/2026_07 combinatorics demo — corpus not yet APPROVED"


@dataclass(frozen=True)
class Combination:
    id: str
    task: str
    context: str
    scenario: str
    rationale: str


COMBINATIONS: tuple[Combination, ...] = (
    # navigate_lead_agent x guidance_docent -- direct role match
    # (leader <-> guide/escort). Museum-docent territory.
    Combination(
        id="lead_docent_leading",
        task="navigate_lead_agent",
        context="guidance_docent",
        scenario="leading",
        rationale=(
            "Scenario text is literally 'a robot in a leader role guides a "
            "human... choosing path and pace' -- the most direct match to "
            "the lead/docent pairing."
        ),
    ),
    Combination(
        id="lead_docent_crowd_navigation",
        task="navigate_lead_agent",
        context="guidance_docent",
        scenario="crowd_navigation",
        rationale=(
            "'Navigates through a crowd... continuously replan' -- the "
            "crowded-museum case for a docent leading a tour."
        ),
    ),
    Combination(
        id="lead_docent_join_a_group",
        task="navigate_lead_agent",
        context="guidance_docent",
        scenario="join_a_group",
        rationale=(
            "'Approach and settle' near a standing group -- a docent "
            "joining a waiting tour group before leading it."
        ),
    ),
    # deliver_object x routine_delivery -- direct role match
    # (transfer object <-> service provider). Office/routine delivery.
    Combination(
        id="deliver_routine_pedestrian_overtaking",
        task="deliver_object",
        context="routine_delivery",
        scenario="pedestrian_overtaking",
        rationale=(
            "Baseline delivery-robot encounter; deliberately paired again "
            "under high_urgency below to demonstrate same scenario+task, "
            "different context."
        ),
    ),
    Combination(
        id="deliver_routine_object_handover",
        task="deliver_object",
        context="routine_delivery",
        scenario="object_handover",
        rationale="Literal handoff scenario, direct fit for a delivery task.",
    ),
    Combination(
        id="deliver_routine_movable_obstruction",
        task="deliver_object",
        context="routine_delivery",
        scenario="movable_obstruction",
        rationale=(
            "Scenario's principle set includes P9, which routine_delivery "
            "emphasizes; deliberately paired again under high_urgency below."
        ),
    ),
    # deliver_object x high_urgency -- high-contrast off-diagonal.
    # This is the literal crash-cart-in-a-hospital case.
    Combination(
        id="deliver_urgent_crash_cart",
        task="deliver_object",
        context="high_urgency",
        scenario="crash_cart",
        rationale=(
            "Scenario text is literally 'delivers an urgent medical "
            "product through... a hospital, moving with elevated pace' -- "
            "no approximation needed, this is the motivating example."
        ),
    ),
    Combination(
        id="deliver_urgent_pedestrian_overtaking",
        task="deliver_object",
        context="high_urgency",
        scenario="pedestrian_overtaking",
        rationale=(
            "Direct contrast against deliver_routine_pedestrian_overtaking: "
            "same scenario + task, only the context changes."
        ),
    ),
    Combination(
        id="deliver_urgent_movable_obstruction",
        task="deliver_object",
        context="high_urgency",
        scenario="movable_obstruction",
        rationale=(
            "Direct contrast against deliver_routine_movable_obstruction: "
            "same scenario + task, only the context changes."
        ),
    ),
    # navigate_follow_agent x public_navigation -- role match
    # (servant/follow <-> neutral baseline).
    Combination(
        id="follow_public_following",
        task="navigate_follow_agent",
        context="public_navigation",
        scenario="following",
        rationale="Scenario text is literally 'robot in servant role follows a human'.",
    ),
    Combination(
        id="follow_public_object_handover",
        task="navigate_follow_agent",
        context="public_navigation",
        scenario="object_handover",
        rationale="Servant-role handoff, contrasts with the delivery-task handover pairing above.",
    ),
    Combination(
        id="follow_public_join_a_group",
        task="navigate_follow_agent",
        context="public_navigation",
        scenario="join_a_group",
        rationale="Following someone into a group setting, contrasts with the lead/docent group pairing above.",
    ),
    # navigate_point_to_point x public_navigation -- neutral/neutral control.
    Combination(
        id="pointtopoint_public_frontal_approach",
        task="navigate_point_to_point",
        context="public_navigation",
        scenario="frontal_approach",
        rationale="Canonical narrow-hallway encounter; a neutral baseline.",
    ),
    Combination(
        id="pointtopoint_public_intersection_no_gesture",
        task="navigate_point_to_point",
        context="public_navigation",
        scenario="intersection_no_gesture",
        rationale="Coordination without explicit signaling; a neutral baseline.",
    ),
    Combination(
        id="pointtopoint_public_single_file_hallway",
        task="navigate_point_to_point",
        context="public_navigation",
        scenario="single_file_hallway",
        rationale="Narrow-passage baseline.",
    ),
)
