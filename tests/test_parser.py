import argparse
import unittest

from chromie.parser import parse_args
from tests.utils import ParserHelper


class TestArgumentParser(unittest.TestCase):
    def test_init_required_arguments(self):
        args = ParserHelper.get_mocked_args("chromie init . -n testy")
        self.assertEqual(args.name, "testy")
        self.assertEqual(args.command, "init")
        self.assertEqual(args.filepath, ".")

    def test_init_overwrite(self):
        args = ParserHelper.get_mocked_args("chromie init . -o")
        self.assertTrue(args.overwrite)

    def test_init_name(self):
        args = ParserHelper.get_mocked_args("chromie init . -n testy")
        self.assertEqual(args.name, "testy")

    def test_pack_required_arguments(self):
        args = ParserHelper.get_mocked_args("chromie pack ./testy")
        self.assertEqual(args.command, "pack")
        self.assertEqual(args.filepath, "./testy")

    def test_pack_args_specific_version(self):
        args = ParserHelper.get_mocked_args("chromie pack ./testy -v 0.0.8")
        self.assertEqual(args.version, "0.0.8")

    def test_pack_args_increment_version(self):
        args = ParserHelper.get_mocked_args("chromie pack ./testy -i patch")
        self.assertEqual(args.increment_version, "patch")


if __name__ == "__main__":
    unittest.main()
