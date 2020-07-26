import argparse
import unittest
from unittest.mock import patch, Mock

from chromie import main
from tests.utils import ParserHelper


class TestMain(unittest.TestCase):
    def test_without_arguments(self):
        with self.assertRaises(SystemExit):
            main([])

    def test_init_missing_filepath(self):
        with self.assertRaises(SystemExit):
            main(["init"])

    @patch("chromie.do_init")
    def test_init(self, init):
        cmd = "chromie init . -n testy"
        argv = ParserHelper.get_argv(cmd)
        mocked_args = ParserHelper.parse_args(
            command="init", filepath=".", name="testy", overwrite=False
        )
        main(argv)

        init.assert_called_with(mocked_args)

    def test_pack_missing_filepath(self):
        with self.assertRaises(SystemExit):
            main(["pack"])

    @patch("chromie.do_pack")
    def test_pack(self, package):
        cmd = "chromie pack ./testy"
        argv = ParserHelper.get_argv(cmd)
        mocked_args = ParserHelper.parse_args(
            command="pack", filepath="./testy", increment_version=None, version=None
        )
        main(argv)

        package.assert_called_with(mocked_args)

    def test_with_invalid_command(self):
        with self.assertRaises(SystemExit):
            main(["thisisnotarealcommand"])


if __name__ == "__main__":
    unittest.main()
