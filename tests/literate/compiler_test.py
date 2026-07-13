# Unit tests for prosoc.literate.compiler

import json
import tempfile
import unittest
from pathlib import Path

from prosoc.literate import compiler
from prosoc.literate import errors

VALID_MARKDOWN = """
# Example Document

```yaml
id: A1
name: First Item
value: 1
```

```yaml
id: A2
name: Second Item
value: 2
```
"""


INVALID_MARKDOWN_NO_YAML = """
# No YAML here

Just some prose.
"""


INVALID_YAML_MARKDOWN = """
```yaml
id A1
name: Missing colon
```
"""


NON_MAPPING_YAML_MARKDOWN = """
```yaml
- just
- a
- list
```
"""


INVALID_SCHEMA_MARKDOWN = """
```yaml
id: A1
name: Missing value field
```
"""


def minimal_schema():
    """
    Minimal JSON schema sufficient for compiler tests.
    """
    return {
        "type": "object",
        "required": ["items"],
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "name", "value"],
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "value": {"type": "number"},
                    },
                },
            }
        },
    }


class TestExtractYamlBlocks(unittest.TestCase):

    def test_extracts_multiple_blocks(self):
        blocks = compiler.extract_yaml_blocks(VALID_MARKDOWN)
        self.assertEqual(len(blocks), 2)

    def test_raises_if_no_yaml_blocks(self):
        with self.assertRaises(errors.LiterateSourceError):
            compiler.extract_yaml_blocks(INVALID_MARKDOWN_NO_YAML)


class TestParseYamlBlocks(unittest.TestCase):

    def test_parses_valid_yaml_blocks(self):
        blocks = compiler.extract_yaml_blocks(VALID_MARKDOWN)
        parsed = compiler.parse_yaml_blocks(blocks)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]["id"], "A1")

    def test_invalid_yaml_raises_yaml_error(self):
        blocks = compiler.extract_yaml_blocks(INVALID_YAML_MARKDOWN)
        with self.assertRaises(errors.LiterateYamlError):
            compiler.parse_yaml_blocks(blocks)

    def test_non_mapping_yaml_raises_structure_error(self):
        blocks = compiler.extract_yaml_blocks(NON_MAPPING_YAML_MARKDOWN)
        with self.assertRaises(errors.LiterateStructureError):
            compiler.parse_yaml_blocks(blocks)


class TestAssembleDocument(unittest.TestCase):

    def test_assemble_document_with_valid_root_key(self):
        items = [{"id": "A1"}, {"id": "A2"}]
        doc = compiler.assemble_document(items, root_key="items")
        self.assertIn("items", doc)
        self.assertEqual(len(doc["items"]), 2)

    def test_invalid_root_key_raises_structure_error(self):
        with self.assertRaises(errors.LiterateStructureError):
            compiler.assemble_document([], root_key="")


class TestSchemaValidation(unittest.TestCase):

    def test_valid_document_passes_schema(self):
        document = compiler.compile_markdown(
            VALID_MARKDOWN,
            schema=minimal_schema(),
            root_key="items",
        )
        self.assertIn("items", document)

    def test_invalid_document_fails_schema(self):
        with self.assertRaises(errors.LiterateSchemaError):
            compiler.compile_markdown(
                INVALID_SCHEMA_MARKDOWN,
                schema=minimal_schema(),
                root_key="items",
            )


class TestCompileFile(unittest.TestCase):

    def test_compile_file_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            md_path = tmpdir / "doc.md"
            schema_path = tmpdir / "schema.json"

            md_path.write_text(VALID_MARKDOWN, encoding="utf-8")
            schema_path.write_text(
                json.dumps(minimal_schema()),
                encoding="utf-8",
            )

            result = compiler.compile_file(
                md_path,
                schema_path=schema_path,
                root_key="items",
            )

            self.assertIn("items", result)
            self.assertEqual(len(result["items"]), 2)

    def test_compile_file_missing_markdown_raises_io_error(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            schema_path = tmpdir / "schema.json"
            schema_path.write_text(
                json.dumps(minimal_schema()),
                encoding="utf-8",
            )

            with self.assertRaises(errors.LiterateIOError):
                compiler.compile_file(
                    tmpdir / "missing.md",
                    schema_path=schema_path,
                    root_key="items",
                )


if __name__ == "__main__":
    unittest.main()
