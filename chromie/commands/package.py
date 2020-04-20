import os
import sys
from fnmatch import fnmatch
from zipfile import ZipFile

NO_DIST_FOUND = "No dist directory was found in the directory specified."
ZIP_SUCCESSFUL = "{} was packaged successfully!"
ZIPFILE_NAME = "deploy.zip"
IGNORE_FILE = ".zipignore"
DIST_DIR_NAME = "dist"
ROOT = os.path.abspath(os.getcwd())


def package(args):
    # TODO: impliment versioning prompt when running command
    # TODO: impliment --version -v argument for setting the version in manifest.json

    ignore = [IGNORE_FILE, DIST_DIR_NAME]
    # Determine filepath
    filepath = os.path.abspath(args.filepath) if args.filepath else ROOT

    # Set dist folder
    dist = os.path.join(filepath, DIST_DIR_NAME)

    # List items in directory
    directory = os.listdir(filepath)

    # Adding items to ignore list from the .zipignore file
    with open(IGNORE_FILE, "r") as zipignore:
        lines = [line.rstrip() for line in zipignore.readlines()]
        [ignore.append(n) for n in directory for l in lines if fnmatch(n, l)]

    if os.path.isdir(dist):
        zip_filename = ZIPFILE_NAME
        zip_path = os.path.join(dist, zip_filename)
        with ZipFile(zip_path, "w") as zip:
            [zip.write(item) for item in directory if item not in ignore]

        print(ZIP_SUCCESSFUL.format(os.path.abspath(zip_path)))
    else:
        raise SystemError(NO_DIST_FOUND)
