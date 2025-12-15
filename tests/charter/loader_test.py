import json
import tempfile
import unittest
from pathlib import Path

import yaml
from jsonschema import ValidationError as SchemaValidationError

from prosoc.charter import loader
from prosoc.charter.runtime import Charter


VALID_CHARTER = {
    "principles": [
        {
            "id": "P0",
            "name": "Goal Achievement",
            "description": "Robots should achieve goals.",
            "severity": "high",
            "examples": {
                "positive": ["Completes task"],
                "negative": ["Abandons task"],
            },
        },
        {
            "id": "P1",
            "name": "Safety",
            "description": "Robots must not cause harm.",
            "severity": "critical",
            "examples": {
                "positive": ["Avoids collision"],
                "negative": ["Hits human"],
            },
        },
    ]
}


INVALID_CHARTER = {
    "principles": [
        {
            "id": "P0",
            "name": "Goal Achievement",
            "description": "Missing examples field.",
            "severity": "high",
        }
    ]
}


MINIMAL_SCHEMA = {
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


class TestLoader(unittest.TestCase):

    def _write_files(self, tmp: Path, charter: dict, schema: dict):
        charter_path = tmp / "charter.yml"
        schema_path = tmp / "schema.json"

        with charter_path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(charter, f, sort_keys=False)

        with schema_path.open("w", encoding="utf-8") as f:
            json.dump(schema, f)

        return charter_path, schema_path

    def test_load_valid_charter(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            charter_path, schema_path = self._write_files(
                td, VALID_CHARTER, MINIMAL_SCHEMA
            )

            charter = loader.load_charter(
                charter_path=charter_path,
                schema_path=schema_path,
            )

            self.assertIsInstance(charter, Charter)
            self.assertEqual(len(charter.principles), 2)
            self.assertEqual(charter.principles[0].id, "P0")

    def test_load_invalid_charter_fails_schema(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            charter_path, schema_path = self._write_files(
                td, INVALID_CHARTER, MINIMAL_SCHEMA
            )

            with self.assertRaises(SchemaValidationError):
                loader.load_charter(
                    charter_path=charter_path,
                    schema_path=schema_path,
                )

    def test_missing_charter_file_raises(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            schema_path = td / "schema.json"

            with schema_path.open("w", encoding="utf-8") as f:
                json.dump(MINIMAL_SCHEMA, f)

            with self.assertRaises(FileNotFoundError):
                loader.load_charter(
                    charter_path=td / "charter.yml",
                    schema_path=schema_path,
                )

    def test_missing_schema_file_raises(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            charter_path = td / "charter.yml"

            with charter_path.open("w", encoding="utf-8") as f:
                yaml.safe_dump(VALID_CHARTER, f)

            with self.assertRaises(FileNotFoundError):
                loader.load_charter(
                    charter_path=charter_path,
                    schema_path=td / "schema.json",
                )

    def test_load_principles_helper(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            charter_path, schema_path = self._write_files(
                td, VALID_CHARTER, MINIMAL_SCHEMA
            )

            principles = loader.load_principles(
                charter_path=charter_path,
                schema_path=schema_path,
            )

            self.assertEqual(len(principles), 2)
            self.assertEqual(principles[1].id, "P1")


if __name__ == "__main__":
    unittest.main()
