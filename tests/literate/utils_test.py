# Unit tests for prosoc.literate.utils

import tempfile
import unittest
from pathlib import Path

from prosoc.literate import utils
from prosoc.literate import errors


class TestDumpYaml(unittest.TestCase):

    def test_dump_yaml_basic_structure(self):
        data = {
            "items": [
                {"id": "A1", "value": 1},
                {"id": "A2", "value": 2},
            ]
        }

        yaml_text = utils.dump_yaml(data)

        self.assertIsInstance(yaml_text, str)
        self.assertIn("items:", yaml_text)
        self.assertIn("- id: A1", yaml_text)

    def test_dump_yaml_invalid_object_raises_io_error(self):
        class Unserializable:
            pass

        with self.assertRaises(errors.LiterateIOError):
            utils.dump_yaml(Unserializable())


class TestUnifiedDiff(unittest.TestCase):

    def test_unified_diff_detects_changes(self):
        old = "a: 1\n"
        new = "a: 2\n"

        diff = utils.unified_diff(
            old_text=old,
            new_text=new,
            fromfile="old",
            tofile="new",
        )

        self.assertIn("-a: 1", diff)
        self.assertIn("+a: 2", diff)

    def test_unified_diff_empty_when_no_change(self):
        text = "a: 1\n"
        diff = utils.unified_diff(
            old_text=text,
            new_text=text,
        )

        self.assertEqual(diff, "")


class TestAtomicWrite(unittest.TestCase):

    def test_atomic_write_creates_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "output.yml"
            content = "key: value\n"

            utils.atomic_write(path, content)

            self.assertTrue(path.exists())
            self.assertEqual(path.read_text(encoding="utf-8"), content)

    def test_atomic_write_overwrites_existing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "output.yml"

            utils.atomic_write(path, "old: value\n")
            utils.atomic_write(path, "new: value\n")

            self.assertEqual(
                path.read_text(encoding="utf-8"),
                "new: value\n",
            )

    def test_atomic_write_invalid_path_raises_io_error(self):
        # Attempt to write into a non-existent directory
        bad_path = Path("/nonexistent_dir/output.yml")

        with self.assertRaises(errors.LiterateIOError):
            utils.atomic_write(bad_path, "key: value\n")


if __name__ == "__main__":
    unittest.main()

