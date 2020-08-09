import os
from zipfile import is_zipfile

from chromie.config import Config
from chromie.webstore import GoogleWebStore, GoogleWebStoreError


def get_latest_version(fp):
    archives = [fn for fn in os.listdir(fp) if is_zipfile(os.path.join(fp, fn))]

    archives.sort(reverse=True)
    return os.path.join(fp, archives[0])


def upload(args):
    root = os.path.abspath(args.filepath)

    dist = os.path.join(root, "dist")
    dot_chromie = os.path.join(root, ".chromie")

    if not os.path.isdir(dot_chromie):
        SystemExit(
            "Please create a '.chromie/settings.json' file within the root project directory"
        )

    archive = get_latest_version(dist)

    config_file = Config.from_file(os.path.join(dot_chromie, "settings.json"))

    with GoogleWebStore.session(
        config_file.data["email"], credentials=config_file.data
    ) as session:
        try:
            extension_id = session.upload(archive)
            data = {"extension_id": extension_id}
            config_file.set_values(**data)
        except GoogleWebStoreError as e:
            print(e)

