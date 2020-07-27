import os
import re
from glob import glob
import zipfile

from chromie.utils import ChromiePathFinder, ManifestFile

VERSION_PROMPT = "How would you like to increment the version?\nOptions are either 'major', 'minor', or 'patch': "
INVALID_VERSION_ARGUMENT = (
    "Incorrect version was entered. Please enter either 'major', 'minor' or 'patch'."
)
INVALID_VERSION_PATTERN = (
    "The version provided was not valid. Please see https://semver.org/ for help."
)
NO_DIST_FOUND = "No dist directory was found in the directory specified."
ZIP_SUCCESSFUL = "{} was packaged successfully!"


def is_valid_increment_version(increment_version):
    if increment_version and increment_version.lower() in ("minor", "major", "patch"):
        return True
    return False


def is_valid_version(version):
    pattern = re.compile(
        r"^([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?$"
    )
    return True if version and pattern.match(version) else False


def write_zip(zip, fp, root, name):
    path = os.path.abspath(os.path.join(root, name))
    if os.name == "posix":
        arcname = f"{fp.split('/')[-1]}/{name}"
        zip.write(path, arcname)
    else:
        zip.write(path, os.path.basename(path))


def package_directory(fp, src, target, ignore_paths=None):
    ignore_paths = [] if not ignore_paths else ignore_paths

    with zipfile.ZipFile(target, "w", zipfile.ZIP_STORED) as zip:
        for dirname, subdirs, files in os.walk(src):
            [
                write_zip(zip, fp, dirname, fn)
                for fn in files
                if os.path.join(dirname, fn) not in ignore_paths
            ]
            [
                write_zip(zip, fp, dirname, dn)
                for dn in subdirs
                if os.path.join(dirname, dn) not in ignore_paths
            ]


def package(args):

    filepath = os.path.abspath(args.filepath)
    increment_version = args.increment_version
    version = args.version

    if not version and not increment_version:
        increment_version = input(VERSION_PROMPT)

    finder = ChromiePathFinder(filepath)

    manifest_file = ManifestFile.from_file(finder("manifest"))

    if increment_version and not version:
        if not is_valid_increment_version(increment_version):
            raise SystemExit(INVALID_VERSION_ARGUMENT)
        version = manifest_file.increment_version(increment_version)

    elif version and not increment_version:
        if not is_valid_version(version):
            raise SystemExit(INVALID_VERSION_PATTERN)
        manifest_file.set_version(version)

    dist = finder("dist")
    if not os.path.isdir(dist):
        os.mkdir(dist)

    src = finder("src")
    with open(finder("zipignore"), "r") as zipignore:
        ignore_paths = [
            name
            for pattern in [line.rstrip() for line in zipignore.readlines()]
            for name in glob(os.path.join(filepath, src, pattern))
        ]

        package_directory(
            filepath,
            os.path.join(filepath, src),
            os.path.join(dist, f"{finder.name}-{version}.zip"),
            ignore_paths,
        )
