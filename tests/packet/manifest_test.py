# Unit tests for prosoc.packet.manifest

import unittest

from prosoc.packet.errors import ManifestError
from prosoc.packet.manifest import Member, parse_manifest


class ParseManifestTest(unittest.TestCase):
    def test_valid(self):
        m = parse_manifest(
            {
                "builder": "me",
                "members": [
                    {"family": "charter", "id": "charter"},
                    {"family": "scenarios", "id": "blind_corner"},
                ],
            }
        )
        self.assertEqual(m.builder, "me")
        self.assertEqual(
            m.members,
            (Member("charter", "charter"), Member("scenarios", "blind_corner")),
        )

    def test_builder_optional(self):
        m = parse_manifest({"members": [{"family": "tasks", "id": "deliver_object"}]})
        self.assertIsNone(m.builder)

    def test_not_a_mapping(self):
        with self.assertRaises(ManifestError):
            parse_manifest([1, 2, 3])

    def test_empty_members(self):
        with self.assertRaises(ManifestError):
            parse_manifest({"members": []})

    def test_member_missing_family(self):
        with self.assertRaises(ManifestError):
            parse_manifest({"members": [{"id": "x"}]})

    def test_member_missing_id(self):
        with self.assertRaises(ManifestError):
            parse_manifest({"members": [{"family": "tasks"}]})

    def test_duplicate_member(self):
        with self.assertRaises(ManifestError):
            parse_manifest(
                {
                    "members": [
                        {"family": "tasks", "id": "deliver_object"},
                        {"family": "tasks", "id": "deliver_object"},
                    ]
                }
            )

    def test_builder_must_be_string(self):
        with self.assertRaises(ManifestError):
            parse_manifest({"builder": 5, "members": [{"family": "tasks", "id": "x"}]})


if __name__ == "__main__":
    unittest.main()
