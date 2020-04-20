import argparse

from chromie.commands import init, package


parser = argparse.ArgumentParser(prog="chromie")

subparsers = parser.add_subparsers(help="commands", dest="command")

init_parser = subparsers.add_parser("init", help="initialize project directory")

init_parser.add_argument(
    "-f", "--filepath", help="project directory", action="store", type=str
)

init_parser.add_argument("-n", "--name", help="Project name", action="store", type=str)

package_parser = subparsers.add_parser("package", help="package project directory")

package_parser.add_argument(
    "-f", "--filepath", help="project directory", action="store", type=str
)


def main():

    args = parser.parse_args()

    if not args:
        raise SystemExit()

    elif args.command == "init":
        init(args)

    elif args.command == "package":
        package(args)

    else:
        raise SystemExit()


if __name__ == "__main__":
    main()
