import filecmp
import os
import pathlib
import shutil
import unittest
from glob import glob

from github_actions_docs import generate_docs


class TestGenerateDocs(unittest.TestCase):
    def setUp(self):
        files = glob("tests/sample_input/*.md")
        for sample_file in files:
            shutil.copy(sample_file, "tests/sample_composite_action")

    def tearDown(self):
        files_to_be_deleted = glob("tests/sample_composite_action/*.md")
        for delete_file in files_to_be_deleted:
            os.remove(delete_file)

    def test_generated_docs_no_readme(self):
        generate_docs(
            file_paths=["tests/sample_composite_action/valid.yaml"],
            uses_ref_override="main",
        )
        path = pathlib.Path("tests/sample_composite_action/README.md")
        self.assertTrue(path.is_file())  # generated file exists

        comparison = filecmp.cmp(
            "tests/sample_composite_action/README.md",
            "tests/sample_output/README_OUTPUT.md",
        )
        self.assertTrue(comparison)  # generated file content is as expected

    def test_generated_docs_existing_readme(self):
        generate_docs(
            file_paths=["tests/sample_composite_action/valid.yaml"],
            docs_filename="EXISTING_README.md",
            uses_ref_override="main",
        )
        path = pathlib.Path("tests/sample_composite_action/EXISTING_README.md")
        self.assertTrue(path.is_file())  # generated file exists

        comparison = filecmp.cmp(
            "tests/sample_composite_action/EXISTING_README.md",
            "tests/sample_output/EXISTING_README_OUTPUT.md",
        )
        self.assertTrue(comparison)  # generated file content is as expected

    def test_generate_docs_invalid(self):
        generate_docs(file_paths=["tests/sample_composite_action/invalid.yaml"])
        path = pathlib.Path("tests/sample_composite_action/README.md")
        self.assertFalse(path.is_file())  # file should not exist


if __name__ == "__main__":
    unittest.main()
