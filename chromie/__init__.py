__author__ = "Steffen Andersland"
__version__ = "0.1.10"
__license__ = "MIT"
__email__ = "steffen@andersland.dev"

import sys

from chromie.parser import parse_args
from chromie.commands import (
    do_init,
    do_pack,
    do_preview,
    do_preview,
    do_config,
    do_upload,
    do_update,
    do_publish,
)


def main(argv=None):
    args = parse_args(argv)

    if args.command == "init":
        do_init(args)

    elif args.command == "pack":
        do_pack(args)

    elif args.command == "preview":
        do_preview(args)

    elif args.command == "config":
        do_config(args)

    elif args.command == "upload":
        do_upload(args)

    elif args.command == "update":
        do_update(args)

    elif args.command == "publish":
        do_publish(args)

    else:
        raise SystemExit("No command selected, for help enter: chromie --help")

    return 0


if __name__ == "__main__":

    sys.exit(main(sys.argv[1:]))
