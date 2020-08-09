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

    config_parser = subparsers.add_parser(
        "config", parents=[parent_parser], help="manage config file"
    )

    config_parser.add_argument("name", action="store", type=str)

    config_parser.add_argument("value", action="store", type=str)

    package_parser.add_argument(
        "-v", "--version", help="specify the version", action="store"
    )

    upload_parser = subparsers.add_parser(
        "upload", parents=[parent_parser], help="upload project to web store"
    )

    update_parser = subparsers.add_parser(
        "update", parents=[parent_parser], help="push updates to web store"
    )

    publish_parser = subparsers.add_parser(
        "publish", parents=[parent_parser], help="publish to web store"
    )

    preview_parser = subparsers.add_parser(
        "preview", parents=[parent_parser], help="preview project in browser"
    )
    return parser.parse_args(argv)
