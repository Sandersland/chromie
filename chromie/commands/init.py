import os
import sys
import json
import shutil

from chromie.utils import ChromiePathFinder, ManifestFile


NAME_PROMPT = "What is the name of your project?\nname: "
OVERWRIGHT_PROMPT = (
    "This directory with this name already exists.\n"
    "Would you like to overwrite anyway? Y/N: "
)
AFFERMATIVE = (
    "Y",
    "YES",
)
NEGATIVE = (
    "N",
    "NO",
)


def init(args):

    name = args.name if args.name else input(NAME_PROMPT)
    exist_ok = args.overwrite

    finder = ChromiePathFinder(args.filepath, name)

    if not exist_ok and os.path.exists(finder.root):
        asked = 0
        overwrite_prompt = ""
        while asked <= 3 or overwrite_prompt not in [*AFFERMATIVE, *NEGATIVE]:
            overwrite_prompt = input(OVERWRIGHT_PROMPT).upper()
            asked += 1
            if overwrite_prompt in NEGATIVE or asked >= 3:
                raise SystemExit()

            elif overwrite_prompt in AFFERMATIVE:
                shutil.rmtree(finder.root, ignore_errors=True)
                break
    else:
        shutil.rmtree(finder.root, ignore_errors=True)

    if not os.path.exists(finder.root):

        os.makedirs(finder("web_store"))
        os.makedirs(finder("images"))

        with open(finder("gitignore"), "w") as f:
            f.write("")

        with open(finder("zipignore"), "w") as f:
            # f.writelines(f"\n".join((".zipignore", "dist")))
            f.write("")

        ManifestFile(
            finder("manifest"),
            {"name": name, "manifest_version": 2, "version": "0.0.0"},
        ).write()
