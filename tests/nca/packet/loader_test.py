# Unit tests for prosoc.nca.packet.loader (against the real checked-in corpus).

import unittest

from prosoc.nca.packet.errors import ManifestError, ResolveError
from prosoc.nca.packet.loader import FAMILIES, REPO_ROOT, load_card


class LoaderTest(unittest.TestCase):
    def test_loads_every_family(self):
        # A representative card from each of the five registered families loads,
        # schema-validates, and reports a lifecycle state.
        samples = {
            "scenarios": "intersection_gesture_wait",
            "tasks": "navigate_lead_agent",
            "contexts": "high_urgency",
            "constitutions": "asimov_three_laws",
            "charter": "charter",
        }
        self.assertEqual(set(samples), set(FAMILIES))
        for family, card_id in samples.items():
            card = load_card(family, card_id)
            self.assertEqual(card.family, family)
            self.assertEqual(card.id, card_id)
            self.assertEqual(len(card.sha256), 64)
            self.assertTrue(card.state)
            self.assertIsInstance(card.payload, dict)
            expected_root = (
                FAMILIES[family].root.resolve().relative_to(REPO_ROOT).as_posix()
            )
            self.assertTrue(card.path.startswith(f"{expected_root}/"))

    def test_constitution_state_is_root_wrapped(self):
        # constitutions read state from constitution.state, not top level.
        # asimov_three_laws reached APPROVED in WI-CARD-APPROVAL-PILOT; the
        # exact value doesn't matter to what this test checks (root-wrapped
        # reading, not a specific lifecycle stage), but it must track reality.
        card = load_card("constitutions", "asimov_three_laws")
        self.assertEqual(card.state, "APPROVED")
        self.assertIn("constitution", card.payload)

    def test_charter_single_source(self):
        card = load_card("charter", "charter")
        self.assertEqual(card.path, "src/prosoc/prnc/charter/charter.yml")
        self.assertIn("principles", card.payload)

    def test_unknown_family(self):
        with self.assertRaises(ManifestError):
            load_card("widgets", "x")

    def test_missing_card(self):
        with self.assertRaises(ResolveError):
            load_card("scenarios", "does_not_exist")

    def test_card_id_path_traversal_is_rejected(self):
        # A malicious card_id must not be able to escape the family root.
        # Calls yml_path() directly, not load_card(), so the assertion
        # isolates the containment check: load_card's separate "no card"
        # ResolveError on a nonexistent path would otherwise also raise
        # ResolveError and mask a missing containment guard.
        with self.assertRaises(ResolveError):
            FAMILIES["scenarios"].yml_path("../../etc")

    def test_card_id_absolute_path_is_rejected(self):
        # pathlib's Path.__truediv__ discards the left operand entirely
        # when the right operand is absolute, so an absolute card_id must
        # be caught by the same containment check as a relative traversal.
        with self.assertRaises(ResolveError):
            FAMILIES["scenarios"].yml_path("/etc")


if __name__ == "__main__":
    unittest.main()
