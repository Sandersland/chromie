import sys

from chromie.parser import parse_args
from chromie.commands import init, package, preview


def main(argv=None):
    args = parse_args(argv)

    if args.command == "init":
        init(args)

    elif args.command == "pack":
        package(args)

    elif args.command == "preview":
        preview(args)

    else:
        parser.print_help()

    return 0


if __name__ == "__main__":

    sys.exit(main(sys.argv[1:]))
