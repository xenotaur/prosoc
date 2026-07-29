# Unit tests for prosoc.charter.distill

import json
import tempfile
import unittest
from pathlib import Path

from prosoc.charter import distill
from prosoc.literate import compiler
from prosoc.literate import errors


VALID_MARKDOWN = """
# Test Charter

```yaml
id: P0
name: Goal Achievement
description: Robots should achieve goals.
severity: high
examples:
  positive:
    - Robot reaches destination.
  negative:
    - Robot refuses to move.
```

```yaml
id: P1
name: Safety
description: Robots must not cause harm.
severity: critical
examples:
  positive:
    - Robot stops before collision.
  negative:
    - Robot bumps into person.
```
"""


INVALID_YAML_MARKDOWN = """
```yaml
id: P0
name Goal Achievement   # missing colon
```
"""


INVALID_SCHEMA_MARKDOWN = """
```yaml
id: P0
name: Goal Achievement
description: Missing examples field.
severity: high
```
"""


def minimal_schema():
    """
    Minimal JSON schema sufficient for tests.
    """
    return {
        "type": "object",
        "required": ["principles"],
        "properties": {
            "principles": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "id",
                        "name",
                        "description",
                        "severity",
                        "examples",
                    ],
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "severity": {"type": "string"},
                        "examples": {
                            "type": "object",
                            "required": ["positive", "negative"],
                        },
                    },
                },
            }
        },
    }


class TestDistillMarkdown(unittest.TestCase):

    def test_valid_markdown_distills(self):
        charter = compiler.compile_markdown(
            markdown_text=VALID_MARKDOWN,
            schema=minimal_schema(),
            root_key="principles",
        )

        self.assertIn("principles", charter)
        self.assertEqual(len(charter["principles"]), 2)
        self.assertEqual(charter["principles"][0]["id"], "P0")

    def test_invalid_yaml_raises_parse_error(self):
        with self.assertRaises(errors.LiterateYamlError):
            compiler.compile_markdown(
                markdown_text=INVALID_YAML_MARKDOWN,
                schema=minimal_schema(),
                root_key="principles",
            )

    def test_schema_violation_raises_schema_error(self):
        with self.assertRaises(errors.LiterateSchemaError):
            compiler.compile_markdown(
                markdown_text=INVALID_SCHEMA_MARKDOWN,
                schema=minimal_schema(),
                root_key="principles",
            )


class TestDistillFile(unittest.TestCase):

    def test_distill_file_round_trip(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)

            md_path = td / "charter.md"
            schema_path = td / "schema.json"

            md_path.write_text(VALID_MARKDOWN, encoding="utf-8")
            schema_path.write_text(
                json.dumps(minimal_schema()),
                encoding="utf-8",
            )

            charter = compiler.compile_file(
                md_path=md_path,
                schema_path=schema_path,
                root_key="principles",
            )

            self.assertEqual(len(charter["principles"]), 2)
            self.assertEqual(charter["principles"][1]["id"], "P1")


STATE_BLOCK = """
```yaml
state: DRAFTED
```
"""

CHARTER_MD_WITH_STATE = "# Test Charter\n" + STATE_BLOCK + VALID_MARKDOWN


def schema_with_state():
    """Minimal schema requiring a top-level state alongside principles."""
    schema = minimal_schema()
    schema["required"] = ["state", "principles"]
    schema["properties"]["state"] = {
        "type": "string",
        # Mirror the canonical lifecycle states (prosoc/charter/schema.json /
        # prosoc.utils.cards.status.STATES) so the test schema stays aligned.
        "enum": [
            "DRAFTED",
            "EDITED",
            "AUDITED",
            "APPROVED",
            "VALIDATED",
            "DEPRECATED",
            "RETIRED",
        ],
    }
    return schema


class TestDistillCharter(unittest.TestCase):
    """Exercise distill_charter's document-level state lifting."""

    def _write(self, td, markdown):
        td = Path(td)
        md_path = td / "charter.md"
        schema_path = td / "schema.json"
        md_path.write_text(markdown, encoding="utf-8")
        schema_path.write_text(json.dumps(schema_with_state()), encoding="utf-8")
        return md_path, schema_path

    def test_lifts_state_to_top_level(self):
        with tempfile.TemporaryDirectory() as td:
            md_path, schema_path = self._write(td, CHARTER_MD_WITH_STATE)
            charter = distill.distill_charter(md_path=md_path, schema_path=schema_path)
            self.assertEqual(set(charter), {"state", "principles"})
            self.assertEqual(charter["state"], "DRAFTED")
            # Principles are intact and the state block is not among them.
            self.assertEqual(len(charter["principles"]), 2)
            self.assertEqual(charter["principles"][0]["id"], "P0")
            self.assertTrue(all("id" in p for p in charter["principles"]))

    def test_missing_state_block_raises(self):
        with tempfile.TemporaryDirectory() as td:
            # VALID_MARKDOWN has principle blocks but no state block.
            md_path, schema_path = self._write(td, "# C\n" + VALID_MARKDOWN)
            with self.assertRaises(errors.LiterateStructureError):
                distill.distill_charter(md_path=md_path, schema_path=schema_path)

    def test_duplicate_state_block_raises(self):
        with tempfile.TemporaryDirectory() as td:
            md_path, schema_path = self._write(
                td, "# C\n" + STATE_BLOCK + STATE_BLOCK + VALID_MARKDOWN
            )
            with self.assertRaises(errors.LiterateStructureError):
                distill.distill_charter(md_path=md_path, schema_path=schema_path)


class TestDiscoverCharter(unittest.TestCase):
    def test_returns_single_source_when_present(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "charter.md").write_text("# C", encoding="utf-8")
            sources = distill.discover_charter(root)
            self.assertEqual(len(sources), 1)
            self.assertEqual(sources[0].md_path, root / "charter.md")
            self.assertEqual(sources[0].yml_path, root / "charter.yml")

    def test_returns_empty_when_absent(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(distill.discover_charter(Path(td)), [])


if __name__ == "__main__":
    unittest.main()
