import filecmp
import os
import pathlib
import shutil
import unittest
from glob import glob

from github_actions_docs.lib.generator import generate_docs


class TestGenerateDocs(unittest.TestCase):
    def setUp(self):
        files = glob("tests/input_docs/*.md")
        for sample_file in files:
            shutil.copy(sample_file, "tests/input_files")

    def tearDown(self):
        files_to_be_deleted = glob("tests/input_files/*.md")
        for delete_file in files_to_be_deleted:
            os.remove(delete_file)

    def test_generated_docs_composite_no_readme(self):
        generate_docs(
            file_paths=["tests/input_files/valid_composite.yaml"],
            usage_ref_override="main",
        )
        path = pathlib.Path("tests/input_files/README.md")
        self.assertTrue(path.is_file())  # generated file exists
        comparison = filecmp.cmp(
            "tests/input_files/README.md",
            "tests/output_docs/COMPOSITE_README.md",
        )
        self.assertTrue(comparison)  # generated file content is as expected

    def test_generated_docs_composite_existing_readme(self):
        generate_docs(
            file_paths=["tests/input_files/valid_composite.yaml"],
            docs_filename="EXISTING_README.md",
            usage_ref_override="main",
        )
        path = pathlib.Path("tests/input_files/EXISTING_README.md")
        self.assertTrue(path.is_file())  # generated file exists

        comparison = filecmp.cmp(
            "tests/input_files/EXISTING_README.md",
            "tests/output_docs/EXISTING_README.md",
        )
        self.assertTrue(comparison)  # generated file content is as expected

    def test_generated_docs_composite_existing_not_tags_readme(self):
        generate_docs(
            file_paths=["tests/input_files/valid_composite.yaml"],
            docs_filename="EXISTING_NO_TAGS_README.md",
            usage_ref_override="main",
        )
        path = pathlib.Path("tests/input_files/EXISTING_NO_TAGS_README.md")
        self.assertTrue(path.is_file())  # generated file exists

        comparison = filecmp.cmp(
            "tests/input_files/EXISTING_NO_TAGS_README.md",
            "tests/output_docs/EXISTING_NO_TAGS_README.md",
        )
        self.assertTrue(comparison)  # generated file content is as expected

    def test_generated_docs_workflow_no_readme(self):
        generate_docs(
            file_paths=["tests/input_files/valid_workflow_2.yaml"],
            usage_ref_override="main",
        )
        path = pathlib.Path("tests/input_files/README.md")
        self.assertTrue(path.is_file())  # generated file exists
        comparison = filecmp.cmp(
            "tests/input_files/README.md",
            "tests/output_docs/WORKFLOW_README.md",
        )
        self.assertTrue(comparison)  # generated file content is as expected

    def test_generated_docs_workflow_update_readme(self):
        generate_docs(
            file_paths=["tests/input_files/valid_workflow_1.yaml"],
            usage_ref_override="main",
        )
        generate_docs(
            file_paths=["tests/input_files/valid_workflow_2.yaml"],
            usage_ref_override="main",
        )
        generate_docs(
            file_paths=["tests/input_files/valid_workflow_1.yaml"],
            usage_ref_override="main",
        )
        path = pathlib.Path("tests/input_files/README.md")
        self.assertTrue(path.is_file())  # generated file exists

        comparison = filecmp.cmp(
            "tests/input_files/README.md",
            "tests/output_docs/WORKFLOW_UPDATE_README.md",
        )
        self.assertTrue(comparison)  # generated file content is as expected

    def test_generated_docs_workflow_existing_readme(self):
        generate_docs(
            file_paths=["tests/input_files/valid_workflow_2.yaml"],
            docs_filename="EXISTING_README.md",
            usage_ref_override="main",
        )
        path = pathlib.Path("tests/input_files/EXISTING_README.md")
        self.assertTrue(path.is_file())  # generated file exists

        comparison = filecmp.cmp(
            "tests/input_files/EXISTING_README.md",
            "tests/output_docs/WORKFLOW_EXISTING_README.md",
        )
        self.assertTrue(comparison)  # generated file content is as expected

    def test_generate_docs_invalid(self):
        generate_docs(file_paths=["tests/input_files/invalid.yaml"])
        path = pathlib.Path("tests/input_files/README.md")
        self.assertFalse(path.is_file())  # file should not exist


if __name__ == "__main__":
    unittest.main()
