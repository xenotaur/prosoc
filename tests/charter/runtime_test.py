import unittest

from prosoc.charter.runtime import (
    ExampleSet,
    CharterPrinciple,
    Charter,
)


class TestExampleSet(unittest.TestCase):

    def test_example_set_construction(self):
        examples = ExampleSet(
            positive=["Does the right thing"],
            negative=["Does the wrong thing"],
        )

        self.assertEqual(len(examples.positive), 1)
        self.assertEqual(len(examples.negative), 1)


class TestCharterPrinciple(unittest.TestCase):

    def test_hard_constraint_detection(self):
        principle = CharterPrinciple(
            id="P1",
            name="Safety",
            description="Robots must not harm humans.",
            severity="critical",
            examples=ExampleSet(
                positive=["Stops before collision"],
                negative=["Collides with human"],
            ),
        )

        self.assertTrue(principle.is_hard_constraint())
        self.assertFalse(principle.is_soft_constraint())

    def test_soft_constraint_detection(self):
        principle = CharterPrinciple(
            id="P4",
            name="Politeness",
            description="Robots should be polite.",
            severity="medium",
            examples=ExampleSet(
                positive=["Waits its turn"],
                negative=["Cuts in line"],
            ),
        )

        self.assertFalse(principle.is_hard_constraint())
        self.assertTrue(principle.is_soft_constraint())


class TestCharterContainer(unittest.TestCase):

    def setUp(self):
        self.charter = Charter(
            principles=[
                CharterPrinciple(
                    id="P0",
                    name="Goal Achievement",
                    description="Robots should achieve goals.",
                    severity="high",
                    examples=ExampleSet(
                        positive=["Completes task"],
                        negative=["Abandons task"],
                    ),
                ),
                CharterPrinciple(
                    id="P1",
                    name="Safety",
                    description="Robots must not cause harm.",
                    severity="critical",
                    examples=ExampleSet(
                        positive=["Avoids collision"],
                        negative=["Hits human"],
                    ),
                ),
            ]
        )

    def test_lookup_by_id(self):
        p1 = self.charter.by_id("P1")
        self.assertIsNotNone(p1)
        self.assertEqual(p1.name, "Safety")

    def test_lookup_missing_id(self):
        self.assertIsNone(self.charter.by_id("P99"))

    def test_hard_constraints(self):
        hard = self.charter.hard_constraints()
        self.assertEqual(len(hard), 2)

    def test_soft_constraints(self):
        soft = self.charter.soft_constraints()
        self.assertEqual(len(soft), 0)


if __name__ == "__main__":
    unittest.main()
