import os
import sys
import json
from fnmatch import fnmatch
import zipfile

from chromie.utils import ChromiePathFinder, ManifestFile

VERSION_PROMPT = "How would you like to increment the version?\nOptions are either 'major', 'minor', or 'patch': "
INVALID_VERSION_ARGUMENT = (
    "Incorrect version was entered. Please enter either 'major', 'minor' or 'patch'."
)
NO_DIST_FOUND = "No dist directory was found in the directory specified."
ZIP_SUCCESSFUL = "{} was packaged successfully!"


def is_valid_version_arg(increment_version):
    if increment_version and increment_version.lower() in ("minor", "major", "patch"):
        return True
    return False


def package(args):
    # TODO: impliment --version -v argument for setting the version in manifest.json

    filepath = os.path.abspath(args.filepath)
    increment_version = args.increment_version

    if not increment_version:
        increment_version = input(VERSION_PROMPT)

    if not is_valid_version_arg(increment_version):
        raise SystemExit(INVALID_VERSION_ARGUMENT)

    finder = ChromiePathFinder(filepath)
    manifest = ManifestFile.from_file(finder("manifest"))
    manifest.increment_version(increment_version)

    zipignore_file = finder("zipignore")
    ignore = [".gitignore", "dist", ".DS_Store"]

    dist = finder("dist")
    if not os.path.isdir(dist):
        os.mkdir(dist)

    directory = os.listdir(filepath)

    with open(zipignore_file, "r") as zipignore:
        lines = [line.rstrip() for line in zipignore.readlines()]
        [ignore.append(n) for n in directory for l in lines if fnmatch(n, l)]

    with zipfile.ZipFile(
        os.path.join(dist, f"{finder.name}.zip"), "w", zipfile.ZIP_DEFLATED
    ) as zip:

        def write_zip(fp, root, name):
            absname = os.path.abspath(os.path.join(root, name))
            arcname = absname[len(fp) + 1 :]
            zip.write(absname, arcname)

        for item in directory:
            if item not in ignore:
                for dirname, subdirs, files in os.walk(os.path.join(filepath, item)):
                    [write_zip(filepath, dirname, fn) for fn in files]
                    [write_zip(filepath, dirname, d) for d in subdirs]
