import argparse

from chromie.commands import init, package, preview

parser = argparse.ArgumentParser(prog="chromie")

subparsers = parser.add_subparsers(help="desired command to perform", dest="command")

parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument(
    "filepath", help="project directory", action="store", type=str
)

init_parser = subparsers.add_parser(
    "init", parents=[parent_parser], help="initialize project directory"
)

init_parser.add_argument(
    "-n", "--name", help="specify the project name", action="store", type=str
)

init_parser.add_argument(
    "-o",
    "--overwrite",
    help="overwrite files if directory already exists",
    action="store_true",
)

package_parser = subparsers.add_parser(
    "package", parents=[parent_parser], help="package project directory"
)

preview_parser = subparsers.add_parser(
    "preview", parents=[parent_parser], help="preview project in browser"
)


def main():

    args = parser.parse_args()

    if args.command == "init":
        init(args)

    elif args.command == "package":
        package(args)

    elif args.command == "preview":
        preview(args)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
