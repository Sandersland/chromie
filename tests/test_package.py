import zipfile
import unittest
import sys
from unittest.mock import patch, MagicMock

from chromie.commands.package import package, is_valid_version
from chromie.enum import Package
from tests.utils import ParserHelper


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


if __name__ == "__main__":
    unittest.main()
