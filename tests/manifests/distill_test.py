# Unit tests for prosoc.manifests.distill

import json
import tempfile
import unittest
from pathlib import Path

from prosoc.manifests import distill

VALID_MANIFEST_MD = """
# Manifest: Test Manifest

```yaml
id: test_manifest
name: Test Manifest
state: DRAFTED
builder: "test"
members:
  - {family: charter, id: charter}
  - {family: tasks, id: navigate_lead_agent}
```
"""


def minimal_schema():
    return {
        "type": "object",
        "required": ["id", "name", "state", "members"],
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "state": {"type": "string"},
            "builder": {"type": "string"},
            "members": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": ["family", "id"],
                    "properties": {
                        "family": {"type": "string"},
                        "id": {"type": "string"},
                    },
                    "additionalProperties": False,
                },
            },
        },
        "additionalProperties": False,
    }


class DiscoverDirectoryLayoutTest(unittest.TestCase):
    def test_no_match_returns_empty(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(distill.discover_manifests(Path(d)), [])

    def test_discovers_manifest_directories(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "sample_packet").mkdir()
            (root / "sample_packet" / "manifest.md").write_text(
                VALID_MANIFEST_MD, encoding="utf-8"
            )
            # Non-manifest directory (no manifest.md) is not discovered.
            (root / "not_a_manifest").mkdir()

            sources = distill.discover_manifests(root)
            self.assertEqual(len(sources), 1)
            self.assertEqual(sources[0].md_path.parent.name, "sample_packet")
            self.assertEqual(sources[0].yml_path.name, "manifest.yml")


class DistillManifestTest(unittest.TestCase):
    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            card_dir = root / "sample_packet"
            card_dir.mkdir()
            md_path = card_dir / "manifest.md"
            md_path.write_text(VALID_MANIFEST_MD, encoding="utf-8")
            schema_path = root / "schema.json"
            schema_path.write_text(json.dumps(minimal_schema()), encoding="utf-8")

            source = distill.ManifestSource(
                md_path=md_path, yml_path=card_dir / "manifest.yml"
            )
            distill.distill_manifest(
                source, schema_path=schema_path, dry_run=False, show_diffs=False
            )

            self.assertTrue(source.yml_path.exists())
            content = source.yml_path.read_text(encoding="utf-8")
            self.assertIn("id: test_manifest", content)
            self.assertIn("family: charter", content)


if __name__ == "__main__":
    unittest.main()
