import shutil
import os
from pathlib import Path as Pa

from chromie.utils import ChromiePathFinder, ManifestFile
from chromie.enum import Initialize, Path


def make_extension_dir(finder):
    for d in [Path.DIST_DIR, Path.SRC_DIR, Path.STORE_DIR, Path.IMAGES_DIR]:
        p = Pa(os.path.join(finder.root, d))
        p.mkdir(parents=True)

    with open(finder(Path.IGNORE_FILE), "w") as f:
        f.write("")

    ManifestFile(
        finder(Path.MANIFEST_FILE),
        {"name": finder.name, "manifest_version": 2, "version": "0.0.0"},
    ).write()


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
        make_extension_dir(finder)
