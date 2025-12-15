import unittest
from pathlib import Path

from jsonschema import ValidationError as SchemaValidationError

import prosoc
from prosoc.charter import distill
from prosoc.charter import loader


class TestCharterFilesWellFormed(unittest.TestCase):
    """
    Guardrail tests ensuring that the on-disk charter artifacts
    (charter.md and charter.yml) are mutually consistent and well-formed.

    These tests are intentionally *integration-level* and operate on the
    repository's canonical files, not temporary fixtures.

    If any of these tests fail, it usually means someone manually edited
    charter.md or charter.yml without running scripts/distill.
    """

    def setUp(self):
        charter_dir = Path(prosoc.__file__).parent / "charter"
        self.charter_md = charter_dir / "charter.md"
        self.charter_yml = charter_dir / "charter.yml"
        self.schema_json = charter_dir / "schema.json"
    
    # ------------------------------------------------------------------
    # charter.md tests
    # ------------------------------------------------------------------

    def test_charter_md_exists(self):
        self.assertTrue(self.charter_md.exists(), "charter.md must exist")

    def test_charter_md_distills_cleanly(self):
        """
        charter.md should be parseable, valid, and schema-compliant.
        """
        markdown_text = self.charter_md.read_text(encoding="utf-8")
        schema = self.schema_json.read_text(encoding="utf-8")

        charter = distill.distill_markdown_to_yaml(
            markdown_text,
            schema=distill.json.loads(schema),
        )

        self.assertIn("principles", charter)
        self.assertGreater(len(charter["principles"]), 0)

    # ------------------------------------------------------------------
    # charter.yml tests
    # ------------------------------------------------------------------

    def test_charter_yml_exists(self):
        self.assertTrue(self.charter_yml.exists(), "charter.yml must exist")

    def test_charter_yml_loads_via_loader(self):
        """
        charter.yml should load cleanly through the schema gate and runtime.
        """
        charter = loader.load_charter(
            charter_path=self.charter_yml,
            schema_path=self.schema_json,
        )

        self.assertGreater(len(charter.principles), 0)

    # ------------------------------------------------------------------
    # Consistency tests
    # ------------------------------------------------------------------

    def test_charter_md_and_yml_are_consistent(self):
        """
        Distilling charter.md should reproduce charter.yml exactly
        (canonical YAML serialization).
        """
        # Distill from Markdown
        distilled = distill.distill_file(
            md_path=self.charter_md,
            schema_path=self.schema_json,
        )
        distilled_text = distill.serialize_charter(distilled)

        # Load existing charter.yml text
        existing_text = self.charter_yml.read_text(encoding="utf-8")

        self.assertEqual(
            distilled_text.strip(),
            existing_text.strip(),
            "charter.md and charter.yml are out of sync; run scripts/distill",
        )


if __name__ == "__main__":
    unittest.main()