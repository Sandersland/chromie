import sys
import argparse
from unittest.mock import patch

from chromie.parser import parse_args


class ParserHelper:
    @classmethod
    def get_mocked_args(cls, cmd):
        argv = cls.get_argv(cmd)
        with patch.object(sys, "argv", argv):
            return parse_args(argv=sys.argv)

    @classmethod
    def get_argv(cls, cmd):
        return cmd.split()[1:]

    @classmethod
    def parse_args(cls, **kwargs):
        return argparse.Namespace(**kwargs)
