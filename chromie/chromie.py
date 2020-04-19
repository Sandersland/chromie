import sys
import os
from typing import List

from chromie.commands import init, package

USAGE = """
Usage: chromie init [--help]
   or: chromie package [--help]
""".strip()

def main():
    args = sys.argv[1:]

    if not args:
        raise SystemExit(USAGE)

    if args[0] == "--help":
        print(USAGE, file=sys.stdout)

    elif args[0] == "init":
        init()

    elif args[0] == "package":
        package()

    else:
        raise SystemExit(USAGE)
    

if __name__ == '__main__':
    main()