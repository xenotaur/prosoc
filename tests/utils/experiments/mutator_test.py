import unittest

from prosoc.utils.experiments import mutator


class TestReplaceYamlBlock(unittest.TestCase):
    """Unit tests for replace_yaml_block utility."""

    def test_replace_yaml_block_preserves_markdown_and_replaces_yaml(self):
        original_markdown = (
            "# Scenario Title\n"
            "\n"
            "Some introductory prose describing the scenario.\n"
            "\n"
            "```yaml\n"
            "id: original_id\n"
            "name: Original Scenario\n"
            "value: 1\n"
            "```\n"
            "\n"
            "Some concluding prose after the YAML block.\n"
        )

        new_yaml = {
            "id": "scrambled_id",
            "name": "Scrambled Scenario",
            "value": 42,
        }

        mutated = mutator.replace_yaml_block(original_markdown, new_yaml)

        # Prose before YAML should be preserved
        self.assertIn("Some introductory prose describing the scenario.", mutated)

        # Prose after YAML should be preserved
        self.assertIn("Some concluding prose after the YAML block.", mutated)

        # Old YAML content should be gone
        self.assertNotIn("original_id", mutated)
        self.assertNotIn("Original Scenario", mutated)

        # New YAML content should be present
        self.assertIn("id: scrambled_id", mutated)
        self.assertIn("name: Scrambled Scenario", mutated)
        self.assertIn("value: 42", mutated)

    def test_missing_yaml_block_raises_error(self):
        markdown_without_yaml = "# No YAML here\nJust prose."

        with self.assertRaises(mutator.YamlBlockNotFoundError):
            mutator.replace_yaml_block(markdown_without_yaml, {"id": "x"})

    def test_multiple_yaml_blocks_raises_error(self):
        markdown_with_two_yaml_blocks = (
            "```yaml\n" "id: one\n" "```\n" "\n" "```yaml\n" "id: two\n" "```\n"
        )

        with self.assertRaises(mutator.MultipleYamlBlocksError):
            mutator.replace_yaml_block(markdown_with_two_yaml_blocks, {"id": "x"})


if __name__ == "__main__":
    unittest.main()
