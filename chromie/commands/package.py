import os
import sys
from fnmatch import fnmatch
from zipfile import ZipFile

from chromie.utils import ChromiePathFinder

NO_DIST_FOUND = "No dist directory was found in the directory specified."
ZIP_SUCCESSFUL = "{} was packaged successfully!"


def package(args):
    # TODO: impliment versioning prompt when running command
    # TODO: impliment --version -v argument for setting the version in manifest.json

    # Determine filepath
    filepath = os.path.abspath(args.filepath)
    finder = ChromiePathFinder(filepath)

    zipignore_file = finder("zipignore")
    dist = finder("dist")

    ignore = [".zipignore", "dist"]
    # Set dist folder
    if not os.path.isdir(dist):
        os.mkdir(dist)

    # List items in directory
    directory = os.listdir(filepath)

    # Adding items to ignore list from the .zipignore file
    with open(zipignore_file, "r") as zipignore:
        lines = [line.rstrip() for line in zipignore.readlines()]
        [ignore.append(n) for n in directory for l in lines if fnmatch(n, l)]

    with ZipFile(os.path.join(dist, f"{finder.name}.zip"), "w") as zip:
        [zip.write(filepath, item) for item in directory if item not in ignore]
