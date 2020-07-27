import unittest
from unittest.mock import patch, Mock

from chromie.commands.init import init, OVERWRIGHT_PROMPT, NAME_PROMPT
from chromie.utils import ChromiePathFinder
from tests.utils import ParserHelper


class TestInit(unittest.TestCase):
    @patch("chromie.commands.init.make_extension_dir")
    @patch("chromie.commands.init.ChromiePathFinder.exists", return_value=False)
    def test_init_makes_directory(self, mocked_exists, mocked_make_extension_dir):

        args = ParserHelper.get_mocked_args("chromie init . -n testy -o")
        finder = ChromiePathFinder(args.filepath, args.name)
        init(args)

        mocked_make_extension_dir.assert_called_with(finder)

    @patch("chromie.commands.init.ChromiePathFinder.exists", return_value=True)
    @patch("builtins.input", return_value="y")
    def test_init_prompts_for_overwrite(self, mocked_input, mocked_exists):
        args = ParserHelper.get_mocked_args("chromie init . -n testy")
        init(args)
        mocked_input.assert_called_with(OVERWRIGHT_PROMPT)

    @patch("builtins.input", return_value="testy")
    def test_init_prompts_for_name(self, mocked_input):
        args = ParserHelper.get_mocked_args("chromie init .")
        init(args)
        mocked_input.assert_called_with(NAME_PROMPT)


if __name__ == "__main__":
    unittest.main()
