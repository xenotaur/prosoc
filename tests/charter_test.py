import unittest
from pathlib import Path
from prosoc import charter
from pydantic import ValidationError


class TestCharterLoading(unittest.TestCase):

    def setUp(self):
        """Set up the path to the test charter file."""
        self.default_path = Path(__file__).parent.parent / "prosoc" / "charter.yml"

    def test_load_charter_success(self):
        """Test that the charter loads and validates correctly."""
        principles = charter.load_charter(self.default_path)
        self.assertGreater(len(principles), 0, "Charter should contain at least one principle")

        for principle in principles:
            self.assertTrue(principle.id.startswith("P"), "Principle ID should start with 'P'")
            self.assertIsInstance(principle.name, str)
            self.assertIsInstance(principle.description, str)
            self.assertIsInstance(principle.examples.positive, list)
            self.assertIsInstance(principle.examples.negative, list)

    def test_charter_validation_failure(self):
        """Test that invalid input raises a ValidationError."""
        # Create a temporary invalid YAML-like dict
        broken_charter = {
            "principles": [
                {
                    "id": "PX",
                    "name": "Missing Description Field",
                    # intentionally omitting 'description' and 'examples'
                }
            ]
        }

        with self.assertRaises(ValidationError):
            charter.Charter(**broken_charter)

    def test_principle_structure(self):
        """Check that each principle has required fields with correct types."""
        principles = charter.load_charter(self.default_path)
        for p in principles:
            self.assertIsInstance(p.id, str)
            self.assertIsInstance(p.name, str)
            self.assertIsInstance(p.description, str)
            self.assertTrue(p.examples.positive or p.examples.negative, "Principle must have at least one example")


if __name__ == "__main__":
    unittest.main()
