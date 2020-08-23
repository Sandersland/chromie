import shutil
import os

from chromie.utils import ChromiePathFinder, ManifestFile
from chromie.enum import Initialize, Path


def make_ignore_file(root):
    with open(os.path.join(root, Path.IGNORE_FILE), "w") as f:
        f.write("")


def make_extension_dir(root, name):
    absroot = os.path.abspath(root)
    os.makedirs(os.path.join(absroot, Path.STORE_DIR))
    os.makedirs(os.path.join(absroot, Path.IMAGES_DIR))

    make_ignore_file(absroot)

    manifest = ManifestFile(
        os.path.join(absroot, Path.MANIFEST_FILE),
        {"name": name, "manifest_version": 2, "version": "0.0.0"},
    )
    manifest.write()


def init(args):

    name = args.name if args.name else input(Initialize.NAME_PROMPT)
    overwrite = args.overwrite

    finder = ChromiePathFinder(args.filepath, name)

    if not overwrite and finder.exists() == True:
        asked = 0
        overwrite_prompt = ""
        while asked <= 3 or overwrite_prompt not in [
            *Initialize.AFFERMATIVE,
            *Initialize.NEGATIVE,
        ]:
            overwrite_prompt = input(Initialize.OVERWRIGHT_PROMPT).upper()
            asked += 1
            if overwrite_prompt in Initialize.NEGATIVE or asked >= 3:
                raise SystemExit()

            elif overwrite_prompt in Initialize.AFFERMATIVE:
                shutil.rmtree(finder.root, ignore_errors=True)
                break

    elif overwrite == True:
        shutil.rmtree(finder.root, ignore_errors=True)

    if not finder.exists(finder.root):
        make_extension_dir(finder.root, finder.name)
