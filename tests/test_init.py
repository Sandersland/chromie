import unittest
from unittest.mock import patch, Mock, call, mock_open
import os

from chromie.commands.init import _mkfile, make_extension_dir, init
from chromie.enum import Initialize, Path
from chromie.utils import ChromiePathFinder
from tests.utils import ParserHelper


class TestInit(unittest.TestCase):
    def test_mkfile(self):
        args = ParserHelper.get_mocked_args("chromie init -n testy -o")
        finder = ChromiePathFinder(args.filepath, args.name)
        path = os.path.join(finder.root, Path.IGNORE_FILE)
        m = mock_open()
        with patch("chromie.commands.init.open", m, create=True):
            _mkfile(path)
            m.assert_called_once_with(path, "w")
            handle = m()
            handle.write.assert_called_once_with("")

    @patch("chromie.commands.init._mkfile")
    @patch("chromie.commands.init.ManifestFile.write")
    @patch("chromie.commands.init.os.makedirs")
    def test_make_extension_dir(
        self, mocked_makedirs, mocked_manifest_write, mocked_mkfile
    ):
        args = ParserHelper.get_mocked_args("chromie init -n testy -o")
        finder = ChromiePathFinder(args.filepath, args.name)

        make_extension_dir(finder)
        self.assertEqual(mocked_makedirs.call_count, 2)
        mocked_makedirs.assert_has_calls(
            [
                call(os.path.join(finder.root, Path.STORE_DIR)),
                call(os.path.join(finder.root, Path.IMAGES_DIR)),
            ],
        )
        mocked_mkfile.assert_called_with(os.path.join(finder.root, Path.IGNORE_FILE))

    @patch("chromie.commands.init.make_extension_dir")
    @patch("chromie.commands.init.ChromiePathFinder.exists", return_value=False)
    def test_init_makes_directory(self, mocked_exists, mocked_make_extension_dir):

        args = ParserHelper.get_mocked_args("chromie init -n testy -o")
        finder = ChromiePathFinder(args.filepath, args.name)
        init(args)

        mocked_make_extension_dir.assert_called_with(finder)

    @patch("chromie.commands.init.make_extension_dir")
    @patch("chromie.commands.init.ChromiePathFinder.exists", return_value=True)
    @patch("chromie.commands.init.input", return_value="y")
    def test_init_prompts_for_overwrite(
        self, mocked_input, mocked_exists, mocked_make_extension_dir
    ):
        args = ParserHelper.get_mocked_args("chromie init -n testy")
        init(args)
        mocked_input.assert_called_with(Initialize.OVERWRIGHT_PROMPT)
        mocked_make_extension_dir.assert_called_once()

    @patch("chromie.commands.init.make_extension_dir")
    @patch("chromie.commands.init.input", return_value="testy")
    def test_init_prompts_for_name(self, mocked_input, mocked_make_extension_dir):
        args = ParserHelper.get_mocked_args("chromie init")
        init(args)
        mocked_input.assert_called_with(Initialize.NAME_PROMPT)
        mocked_make_extension_dir.assert_called_once()


if __name__ == "__main__":
    unittest.main()
