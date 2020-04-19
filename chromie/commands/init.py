import os
import sys
import json


ROOT = os.path.abspath(os.getcwd())
NEW_DIRS = ("dist", "images", "images/web store",)
NEW_BLANK_FILES = (".gitignore", ".zipignore")
MANIFEST_FILE = "manifest.json"
NAME_PROMPT = "What is the name of your project?\nname: "
OVERWRITE_PROMPT = "This file or directory {} already exists.\nType (Y)es to overwrite. "
AFFERMATIVE = ("Y", "YES",)
NEGATIVE = ("N", "NO")
TASK_COMPLETED = "Job completed."
TASK_ABORTED = "Job aborted."
FILES_CREATED = "The following files or directories were created:\n"


def prompt_overwrite(path):
    #TODO: prevent this if -y is in argv
    #TODO: make wrapper for this instead
    repeat = 0
    overwrite = input(OVERWRITE_PROMPT.format(path)).upper()
    repeat += 1
    try:
        while overwrite not in (*AFFERMATIVE, *NEGATIVE) or repeat <= 3:
            if overwrite in NEGATIVE:
                raise SystemExit(TASK_ABORTED)
            elif overwrite in AFFERMATIVE:
                break
            else:
                overwrite = input(OVERWRITE_PROMPT.format(path)).upper()
                repeat += 1
    except KeyboardInterrupt as e:
        raise SystemExit(e)


def init():
    #TODO: impliment -f argument to specify directory and skip prompt if present
    created = []
    name = input(NAME_PROMPT)
    root = os.path.join(ROOT, name)

    if not os.path.isdir(root):
        os.mkdir(root)
        created.append(root)

    for folder_name in NEW_DIRS:
        folderpath = os.path.join(root, folder_name)
        if not os.path.isdir(folderpath):
            os.mkdir(folderpath)
            created.append(folderpath)
    
    for file_name in NEW_BLANK_FILES:
        filepath = os.path.join(root, file_name)
        if not os.path.isfile(filepath):
            with open(filepath, 'w') as f:
                f.write("")
            created.append(filepath)
        else:
            prompt_overwrite(filepath)

    manifest = os.path.join(root, MANIFEST_FILE)
    if not os.path.isfile(manifest):
        with open(manifest, 'w') as f:
            json.dump(
                {
                    "name": name,
                    "manifest_version": 2,
                    "version": "0.1.0"
                }, f, indent=2
            )
        created.append(manifest)
    else:
        prompt_overwrite(manifest)

    if len(created) > 0:
        print(FILES_CREATED + f"\n".join([dir for dir in created]), 
            file=sys.stdout
        )
    print(TASK_COMPLETED)
