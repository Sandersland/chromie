import zipfile
import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import tempfile

from chromie.commands.package import package, is_valid_version, filterdir, listdir
from chromie.enum import Package
from tests.utils import ParserHelper


def mktempdirectory(directories: list, files: list = []):
    if not directories:
        raise Exception(
            "Please include at least one directory name when invoking this method"
        )
    root = tempfile.mkdtemp()
    for d in directories:
        os.makedirs(os.path.join(root, d))

    for file in files:
        with open(os.path.join(root, file), "w") as f:
            f.write("")
    return root


def call_package(argv):
    args = ParserHelper.get_mocked_args(argv)
    try:
        package(args)
    except:
        pass


class TestPackage(unittest.TestCase):
    def setUp(self):
        self.version = "0.0.1"

    @patch("builtins.input", return_value="patch")
    def test_package_prompts_for_version_type(self, mocked_input):
        call_package("chromie pack")
        mocked_input.assert_called_with(Package.VERSION_PROMPT)

    def test_is_valid_version_true(self):
        valid = is_valid_version(self.version)
        self.assertTrue(valid)

    def test_is_valid_version_false(self):
        valid = is_valid_version("0.0.0.0")
        self.assertFalse(valid)

    @patch("chromie.commands.package.ManifestFile.from_file", return_value=MagicMock())
    @patch("chromie.commands.package.is_valid_version", return_value=True)
    def test_is_valid_version_called(self, mocked_is_valid_version, mocked_from_file):
        call_package(f"chromie pack -v {self.version}")
        mocked_is_valid_version.assert_called_with(self.version)

    @patch("chromie.commands.package.ManifestFile.from_file", return_value=MagicMock())
    def test_manifest_file_version_is_set(self, mocked_from_file):
        call_package(f"chromie pack -v {self.version}")
        mocked_from_file.return_value.set_version.assert_called_with(self.version)


class TestFilterDir(unittest.TestCase):
    def setUp(self):
        self.directory = mktempdirectory(
            directories=["test", "help"],
            files=[
                "test/hello.txt",
                "test/hello.html",
                "help/hello.html",
                "help/help.txt",
            ],
        )

    def test_filter_dir(self):
        patterns = ["*.txt"]
        filtered = filterdir(self.directory, patterns)
        self.assertEqual(len(filtered), 4)

    def test_filter_dir_on_directory(self):
        patterns = ["test"]
        filtered = filterdir(self.directory, patterns)
        self.assertEqual(len(filtered), 3)

    def test_filter_dir_on_asterisk(self):
        patterns = ["*"]
        filtered = filterdir(self.directory, patterns)
        self.assertEqual(len(filtered), 0)


class testListDir(unittest.TestCase):
    def setUp(self):
        self.directory = mktempdirectory(
            ["test", "hello", "test/this"],
            ["test/this/file.txt", "test/this/file2.txt"],
        )

    def test_listdir_recursive(self):
        l = listdir(self.directory, recursive=True)
        self.assertEqual(len(l), 5)

    def test_listdir(self):
        l = listdir(self.directory)
        self.assertEqual(len(l), 2)


if __name__ == "__main__":
    unittest.main()
