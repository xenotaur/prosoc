# Unit tests for prosoc.nca.packet.resolve

import unittest

from prosoc.nca.packet.errors import ResolveError
from prosoc.nca.packet.manifest import Manifest, Member
from prosoc.nca.packet.resolve import resolve


class ResolveTest(unittest.TestCase):
    def test_preserves_manifest_order(self):
        manifest = Manifest(
            members=(
                Member("tasks", "navigate_lead_agent"),
                Member("charter", "charter"),
                Member("contexts", "high_urgency"),
            )
        )
        cards = resolve(manifest)
        self.assertEqual(
            [(c.family, c.id) for c in cards],
            [
                ("tasks", "navigate_lead_agent"),
                ("charter", "charter"),
                ("contexts", "high_urgency"),
            ],
        )

    def test_dangling_member_raises(self):
        manifest = Manifest(members=(Member("scenarios", "nope_not_here"),))
        with self.assertRaises(ResolveError):
            resolve(manifest)


if __name__ == "__main__":
    unittest.main()
