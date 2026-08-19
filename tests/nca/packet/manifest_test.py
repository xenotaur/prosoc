# Unit tests for prosoc.nca.packet.manifest

import tempfile
import unittest
from pathlib import Path

from prosoc.nca.packet.errors import ManifestError
from prosoc.nca.packet.manifest import Member, load_manifest, parse_manifest


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


class LoadManifestTest(unittest.TestCase):
    def test_missing_file(self):
        with self.assertRaises(ManifestError):
            load_manifest(Path("/nonexistent/manifest.yml"))

    def test_invalid_utf8_raises_manifest_error(self):
        # A non-UTF-8 file must surface as ManifestError, not UnicodeDecodeError.
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "m.yml"
            p.write_bytes(b"\xff\xfe not utf-8")
            with self.assertRaises(ManifestError):
                load_manifest(p)

    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "m.yml"
            p.write_text(
                "members:\n  - {family: charter, id: charter}\n", encoding="utf-8"
            )
            m = load_manifest(p)
            self.assertEqual(m.members, (Member("charter", "charter"),))


if __name__ == "__main__":
    unittest.main()
