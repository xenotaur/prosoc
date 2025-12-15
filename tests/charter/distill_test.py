import json
import unittest
import tempfile
from pathlib import Path

from jsonschema import ValidationError as SchemaValidationError

from prosoc.charter import distill


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


class TestExtractYamlBlocks(unittest.TestCase):

    def test_extracts_multiple_blocks(self):
        blocks = distill.extract_yaml_blocks(VALID_MARKDOWN)
        self.assertEqual(len(blocks), 2)

    def test_raises_if_no_blocks(self):
        with self.assertRaises(ValueError):
            distill.extract_yaml_blocks("No YAML here.")


class TestParseYamlBlocks(unittest.TestCase):

    def test_parses_valid_blocks(self):
        blocks = distill.extract_yaml_blocks(VALID_MARKDOWN)
        parsed = distill.parse_yaml_blocks(blocks)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]["id"], "P0")

    def test_invalid_yaml_raises(self):
        blocks = distill.extract_yaml_blocks(INVALID_YAML_MARKDOWN)
        with self.assertRaises(ValueError):
            distill.parse_yaml_blocks(blocks)


class TestAssembleCharter(unittest.TestCase):

    def test_assemble_structure(self):
        principles = [{"id": "P0"}, {"id": "P1"}]
        charter = distill.assemble_charter(principles)
        self.assertIn("principles", charter)
        self.assertEqual(len(charter["principles"]), 2)


class TestSchemaValidation(unittest.TestCase):

    def test_valid_charter_passes_schema(self):
        charter = distill.distill_markdown_to_yaml(
            VALID_MARKDOWN,
            minimal_schema(),
        )
        self.assertIn("principles", charter)

    def test_invalid_charter_fails_schema(self):
        with self.assertRaises(SchemaValidationError):
            distill.distill_markdown_to_yaml(
                INVALID_SCHEMA_MARKDOWN,
                minimal_schema(),
            )


class TestDistillFileIntegration(unittest.TestCase):

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

            charter = distill.distill_file(
                md_path=md_path,
                schema_path=schema_path,
            )

            self.assertEqual(len(charter["principles"]), 2)
            self.assertEqual(charter["principles"][0]["id"], "P0")


if __name__ == "__main__":
    unittest.main()
