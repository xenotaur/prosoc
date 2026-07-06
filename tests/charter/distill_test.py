# Unit tests for prosoc.charter.distill

import json
import tempfile
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
