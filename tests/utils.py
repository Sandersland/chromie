import sys
import argparse
from unittest.mock import patch

from chromie.parser import parse_args


class ParserHelper:
    @classmethod
    def get_mocked_args(self, cmd):
        argv = self.get_argv(cmd)
        with patch.object(sys, "argv", argv):
            return parse_args(argv=sys.argv)

    @classmethod
    def get_argv(self, cmd):
        return cmd.split()[1:]

    @classmethod
    def parse_args(self, **kwargs):
        return argparse.Namespace(**kwargs)
