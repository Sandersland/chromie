__author__ = "Steffen Andersland"
__version__ = "0.1.9"
__license__ = "MIT"
__email__ = "stefandersland@gmial.com"

import sys

from chromie.parser import parse_args
from chromie.commands import do_init, do_pack, do_preview


def main(argv=None):
    args = parse_args(argv)

    if args.command == "init":
        do_init(args)

    elif args.command == "pack":
        do_pack(args)

    elif args.command == "preview":
        do_preview(args)

    else:
        raise SystemExit("No command selected, for help enter: chromie --help")

    return 0


if __name__ == "__main__":

    sys.exit(main(sys.argv[1:]))
