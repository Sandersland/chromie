import os
import re
from fnmatch import fnmatch
import zipfile

from chromie.utils import ChromiePathFinder, ManifestFile
from chromie.enum import Package, Path


def is_valid_increment_version(increment_version):
    if increment_version and increment_version.lower() in ("minor", "major", "patch"):
        return True
    return False


def is_valid_version(version):
    pattern = re.compile(
        r"^([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?$"
    )
    return True if version and pattern.match(version) else False


def write_zip(zip, path, name):
    arcname_path = re.search(r"(?<=src).+", path).group(0)
    arcname = os.path.join(name, arcname_path)
    zip.write(path, arcname)


def package_directory(paths, fp, target):
    name = fp.split("/")[-1]
    with zipfile.ZipFile(target, "w", zipfile.ZIP_STORED) as zip:
        for path in paths:
            write_zip(zip, path, name)


def filterdir(root_dir, ignore_patterns):
    matches = []
    flagged_for_removal = []
    directory = listdir(root_dir, True)
    for i, path in enumerate(directory):
        if path in flagged_for_removal:
            matches.append(i)
            continue

        for pat in ignore_patterns:
            pattern = os.path.join("*", pat)
            is_match = fnmatch(path, pattern)
            if is_match and i not in matches:
                matches.append(i)
            if is_match and os.path.isdir(path):
                flagged_for_removal.extend(listdir(path, True))

    for index in sorted(matches, reverse=True):
        del directory[index]

    return directory


def listdir(root_dir: str, recursive: bool = False):
    if not recursive:
        return os.listdir(root_dir)

    paths = []

    for root, dirnames, filenames in os.walk(root_dir):
        paths.extend([os.path.join(root, d) for d in dirnames])
        paths.extend([os.path.join(root, filename) for filename in filenames])

    return sorted(paths)


def package(args):

    filepath = os.path.abspath(args.filepath)
    increment_version = args.increment_version
    version = args.version

    if not version and not increment_version:
        increment_version = input(Package.VERSION_PROMPT)

    finder = ChromiePathFinder(filepath)

    manifest_file = ManifestFile.from_file(finder(Path.MANIFEST_FILE))

    if increment_version and not version:
        if not is_valid_increment_version(increment_version):
            raise SystemExit(Package.INVALID_VERSION_ARGUMENT)
        version = manifest_file.increment_version(increment_version)

    elif version and not increment_version:
        if not is_valid_version(version):
            raise SystemExit(Package.INVALID_VERSION_PATTERN)
        manifest_file.set_version(version)

    dist = finder(Path.DIST_DIR)
    if not os.path.isdir(dist):
        os.mkdir(dist)

    src = finder(Path.SRC_DIR)
    with open(finder(Path.IGNORE_FILE), "r") as zipignore:
        zip_paths = filterdir(src, zipignore.readlines())
        package_directory(
            zip_paths, filepath, os.path.join(dist, f"{finder.name}-{version}.zip"),
        )


if __name__ == "__main__":
    print(Path.MANIFEST_FILE)
