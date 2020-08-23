import unittest
from unittest.mock import patch, Mock, call, mock_open
import os

from chromie.commands.init import *
from chromie.enum import Initialize, Path
from chromie.utils import ChromiePathFinder
from tests.utils import ParserHelper


class TestInit(unittest.TestCase):
    def test_make_ignore_file(self):
        args = ParserHelper.get_mocked_args("chromie init -n testy -o")
        finder = ChromiePathFinder(args.filepath, args.name)
        absroot = os.path.abspath(finder.root)
        m = mock_open()
        with patch("chromie.commands.init.open", m, create=True):
            make_ignore_file(absroot)
            m.assert_called_once_with(os.path.join(absroot, Path.IGNORE_FILE), "w")
            handle = m()
            handle.write.assert_called_once_with("")

    @patch("chromie.commands.init.make_ignore_file")
    @patch("chromie.commands.init.ManifestFile.write")
    @patch("chromie.commands.init.os.makedirs")
    def test_make_extension_dir(
        self, mocked_makedirs, mocked_manifest_write, mocked_make_ignore
    ):
        args = ParserHelper.get_mocked_args("chromie init -n testy -o")
        finder = ChromiePathFinder(args.filepath, args.name)

        make_extension_dir(finder.root, finder.name)
        absroot = os.path.abspath(finder.root)
        self.assertEqual(mocked_makedirs.call_count, 2)
        mocked_makedirs.assert_has_calls(
            [
                call(os.path.join(absroot, Path.STORE_DIR)),
                call(os.path.join(absroot, Path.IMAGES_DIR)),
            ],
        )
        mocked_make_ignore.assert_called_with(os.path.abspath(finder.root))

    @patch("chromie.commands.init.make_extension_dir")
    @patch("chromie.commands.init.ChromiePathFinder.exists", return_value=False)
    def test_init_makes_directory(self, mocked_exists, mocked_make_extension_dir):

        args = ParserHelper.get_mocked_args("chromie init -n testy -o")
        finder = ChromiePathFinder(args.filepath, args.name)
        init(args)

        mocked_make_extension_dir.assert_called_with(finder.root, finder.name)

    @patch("chromie.commands.init.ChromiePathFinder.exists", return_value=True)
    @patch("builtins.input", return_value="y")
    def test_init_prompts_for_overwrite(self, mocked_input, mocked_exists):
        args = ParserHelper.get_mocked_args("chromie init -n testy")
        init(args)
        mocked_input.assert_called_with(Initialize.OVERWRIGHT_PROMPT)

    @patch("builtins.input", return_value="testy")
    def test_init_prompts_for_name(self, mocked_input):
        args = ParserHelper.get_mocked_args("chromie init")
        init(args)
        mocked_input.assert_called_with(Initialize.NAME_PROMPT)


if __name__ == "__main__":
    unittest.main()
