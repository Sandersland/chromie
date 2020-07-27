import argparse

from chromie import __version__


def parse_args(argv=None):
    parser = argparse.ArgumentParser(prog="chromie")

    parser.add_argument(
        "-v", "--version", action="version", version=f"chromie-{__version__}"
    )

    subparsers = parser.add_subparsers(
        help="desired command to perform", dest="command"
    )

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
        "pack", parents=[parent_parser], help="package project directory"
    )

    package_parser.add_argument(
        "-i",
        "--increment-version",
        help="increment project version before packaging based with (major, minor, patch) as options",
        action="store",
    )

    package_parser.add_argument(
        "-v", "--version", help="specify the version", action="store"
    )

    preview_parser = subparsers.add_parser(
        "preview", parents=[parent_parser], help="preview project in browser"
    )
    return parser.parse_args(argv)
