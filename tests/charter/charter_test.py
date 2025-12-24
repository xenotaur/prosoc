# Guardrail tests for prosoc charter consistency

import unittest
from pathlib import Path

import prosoc
from prosoc.charter import loader
from prosoc.literate import compiler, utils


class TestCharterFilesWellFormed(unittest.TestCase):
    """
    Guardrail tests ensuring that:
    - charter.md exists
    - charter.yml exists
    - charter.md distills exactly to charter.yml

    These tests enforce the "single source of truth" invariant:
    charter.md is authoritative, charter.yml must be its canonical derivative.
    """

    def setUp(self):
        # Locate prosoc/charter directory via package import
        charter_dir = Path(prosoc.__file__).parent / "charter"

        self.charter_md = charter_dir / "charter.md"
        self.charter_yml = charter_dir / "charter.yml"
        self.schema_json = charter_dir / "schema.json"

    def test_charter_md_exists(self):
        self.assertTrue(
            self.charter_md.exists(),
            "charter.md must exist in prosoc/charter",
        )

    def test_charter_yml_exists(self):
        self.assertTrue(
            self.charter_yml.exists(),
            "charter.yml must exist in prosoc/charter",
        )

    def test_charter_md_and_yml_are_consistent(self):
        """
        Distilling charter.md should reproduce charter.yml exactly.
        This fails if charter.md is edited without regenerating charter.yml.
        """
        compiled = compiler.compile_file(
            md_path=self.charter_md,
            schema_path=self.schema_json,
            root_key="principles",
        )

        compiled_yaml = utils.dump_yaml(compiled)
        existing_yaml = self.charter_yml.read_text(encoding="utf-8")

        compiled_yaml = utils.dump_yaml(compiled)
        existing_yaml = self.charter_yml.read_text(encoding="utf-8")

        self.assertEqual(
            compiled_yaml,
            existing_yaml,
            "charter.yml is out of sync with charter.md; run scripts/distill",
        )


class TestCharterRuntimeLoading(unittest.TestCase):
    """
    Sanity check that the generated charter.yml loads into runtime models.
    """

    def test_loader_can_load_charter(self):
        charter = loader.load_charter()
        principles = charter.principles


        self.assertGreater(
            len(principles),
            0,
            "Charter should contain at least one principle",
        )

        for principle in principles:
            self.assertTrue(
                principle.id.startswith("P"),
                "Principle ID should start with 'P'",
            )
            self.assertIsInstance(principle.name, str)
            self.assertIsInstance(principle.description, str)
            self.assertTrue(
                principle.examples.positive
                or principle.examples.negative,
                "Principle must have at least one example",
            )


if __name__ == "__main__":
    unittest.main()
