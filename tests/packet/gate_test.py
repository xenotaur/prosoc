# Unit tests for prosoc.packet.gate

import unittest
from types import SimpleNamespace

from prosoc.packet.gate import gate


def _card(state, fam="scenarios", cid="x"):
    return SimpleNamespace(family=fam, id=cid, state=state)


class GateTest(unittest.TestCase):
    def test_all_approved_passes(self):
        result = gate([_card("APPROVED"), _card("VALIDATED", cid="y")])
        self.assertTrue(result.passed)
        self.assertEqual(result.threshold, "APPROVED")
        self.assertEqual(result.blocked, ())

    def test_below_threshold_blocks_fail_closed(self):
        result = gate([_card("APPROVED"), _card("DRAFTED", cid="y")])
        self.assertFalse(result.passed)
        self.assertEqual(len(result.blocked), 1)
        self.assertEqual(result.blocked[0].id, "y")

    def test_allow_unapproved_lifts_pre_approval_states(self):
        result = gate(
            [_card("DRAFTED"), _card("EDITED", cid="y"), _card("AUDITED", cid="z")],
            allow_unapproved=True,
        )
        self.assertTrue(result.passed)
        self.assertEqual(result.threshold, "DRAFTED")

    def test_allow_unapproved_never_ships_end_of_life(self):
        # DEPRECATED / RETIRED are blocked even with the escape hatch.
        for eol in ("DEPRECATED", "RETIRED"):
            result = gate([_card(eol)], allow_unapproved=True)
            self.assertFalse(result.passed, eol)
            self.assertEqual(result.blocked[0].state, eol)

    def test_unknown_state_blocked(self):
        result = gate([_card("BOGUS")], allow_unapproved=True)
        self.assertFalse(result.passed)

    def test_empty_passes(self):
        # Gate over no cards is vacuously satisfied; assemble() guards emptiness.
        self.assertTrue(gate([]).passed)


if __name__ == "__main__":
    unittest.main()
