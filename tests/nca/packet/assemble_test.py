# Unit tests for prosoc.nca.packet.assemble

import hashlib
import json
import unittest

from prosoc.nca.packet.assemble import assemble, validate_envelope
from prosoc.nca.packet.errors import AssembleError
from prosoc.nca.packet.loader import LoadedCard
from prosoc.nca.packet.manifest import Manifest

FAKE_SHA = "0" * 64


def _card(family, cid, payload, state="APPROVED"):
    return LoadedCard(
        family=family,
        id=cid,
        path=f"prosoc/{family}/{cid}.yml",
        sha256=FAKE_SHA,
        state=state,
        payload=payload,
    )


def _charter():
    return _card(
        "charter",
        "charter",
        {
            "state": "APPROVED",
            "principles": [
                {"id": "P0", "name": "Goal"},
                {"id": "P1", "name": "Safety"},
                {"id": "P2", "name": "Comfort"},
                {"id": "P3", "name": "Legibility"},
            ],
        },
    )


def _scenario():
    return _card(
        "scenarios",
        "s1",
        {
            "state": "APPROVED",
            "id": "s1_01",
            # top-level inline context — the collision Decision 5 guards against
            "context": {"environment": {"type": "indoor"}},
            "relevant_principles": ["P0", "P1"],
        },
    )


def _task():
    return _card("tasks", "t1", {"state": "APPROVED", "related_principles": ["P2"]})


def _context():
    return _card(
        "contexts",
        "c1",
        {
            "state": "APPROVED",
            "principle_emphasis": {
                "emphasized": ["P0"],
                "deprioritized": ["P3"],
                "common_tensions": ["speed vs safety"],
            },
        },
    )


def _constitution():
    return _card(
        "constitutions",
        "k1",
        {
            "constitution": {
                "id": "k1",
                "state": "APPROVED",
                "rules": [{"id": "L1"}],
                "conflict_resolution": {"strategy": "priority"},
            }
        },
    )


def _manifest():
    return Manifest(members=(), builder="tester")


class AssembleTest(unittest.TestCase):
    def test_envelope_shape_and_schema(self):
        env = assemble([_charter(), _scenario()], _manifest())
        self.assertEqual(env["_type"], "https://in-toto.io/Statement/v1")
        self.assertEqual(env["signatures"], [])
        # assemble() validates internally; validate_envelope is idempotent here.
        validate_envelope(env)

    def test_namespaced_no_context_collision(self):
        env = assemble([_scenario(), _context()], _manifest())
        g = env["guidance"]
        # The scenario's inline context stays under the scenario; the context
        # card lives under contexts — never merged.
        self.assertIn("context", g["scenarios"]["s1"])
        self.assertIn("c1", g["contexts"])
        self.assertNotEqual(g["scenarios"]["s1"]["context"], g["contexts"]["c1"])

    def test_charter_namespaced_under_id(self):
        # The charter is nested under its id like every other family, so the
        # guidance shape is uniform (family -> id -> body).
        env = assemble([_charter()], _manifest())
        self.assertIn("charter", env["guidance"]["charter"])
        self.assertIn("principles", env["guidance"]["charter"]["charter"])

    def test_state_stripped_from_guidance_kept_in_predicate(self):
        env = assemble([_scenario()], _manifest())
        self.assertNotIn("state", env["guidance"]["scenarios"]["s1"])
        states = {c["id"]: c["state"] for c in env["predicate"]["resolved_cards"]}
        self.assertEqual(states["s1"], "APPROVED")

    def test_constitution_root_normalized(self):
        env = assemble([_constitution()], _manifest())
        body = env["guidance"]["constitutions"]["k1"]
        self.assertNotIn("constitution", body)  # unwrapped
        self.assertNotIn("state", body)  # stripped
        self.assertEqual(body["id"], "k1")

    def test_principle_union_none_dropped(self):
        env = assemble([_charter(), _scenario(), _task(), _context()], _manifest())
        principles = {p["id"]: p["emphasis"] for p in env["guidance"]["principles"]}
        # union of relevant {P0,P1} + related {P2} + emphasized {P0} + depri {P3}
        self.assertEqual(set(principles), {"P0", "P1", "P2", "P3"})
        self.assertEqual(principles["P0"], "emphasized")
        self.assertEqual(principles["P3"], "deprioritized")  # kept, annotated
        self.assertEqual(principles["P1"], "neutral")
        # charter detail joined
        p0 = next(p for p in env["guidance"]["principles"] if p["id"] == "P0")
        self.assertEqual(p0["name"], "Goal")

    def test_tensions_both_surfaced(self):
        env = assemble([_context(), _constitution()], _manifest())
        t = env["guidance"]["tensions"]
        self.assertEqual(len(t["common_tensions"]), 1)
        self.assertEqual(len(t["conflict_resolution"]), 1)

    def test_digest_covers_guidance(self):
        env = assemble([_charter(), _scenario()], _manifest())
        recomputed = hashlib.sha256(
            json.dumps(
                env["guidance"],
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            ).encode("utf-8")
        ).hexdigest()
        self.assertEqual(env["subject"][0]["digest"]["sha256"], recomputed)

    def test_escape_hatch_stamped_into_payload(self):
        env = assemble(
            [_card("scenarios", "s1", {"state": "DRAFTED"}, state="DRAFTED")],
            _manifest(),
            allow_unapproved=True,
            justification="dev packet",
        )
        self.assertIn("notice", env["guidance"])
        hatch = env["predicate"]["policy"]["escape_hatch"]
        self.assertEqual(hatch["justification"], "dev packet")
        self.assertEqual(hatch["cards_below_threshold"][0]["id"], "s1")

    def test_escape_hatch_requires_justification(self):
        with self.assertRaises(AssembleError):
            assemble(
                [_card("scenarios", "s1", {"state": "DRAFTED"}, state="DRAFTED")],
                _manifest(),
                allow_unapproved=True,
                justification=None,
            )

    def test_no_hatch_when_all_approved(self):
        env = assemble([_scenario()], _manifest(), allow_unapproved=True)
        self.assertNotIn("notice", env["guidance"])
        self.assertIsNone(env["predicate"]["policy"]["escape_hatch"])

    def test_empty_raises(self):
        with self.assertRaises(AssembleError):
            assemble([], _manifest())

    def test_validate_rejects_broken_envelope(self):
        with self.assertRaises(AssembleError):
            validate_envelope({"_type": "wrong"})


if __name__ == "__main__":
    unittest.main()
