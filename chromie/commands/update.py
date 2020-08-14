import os
from zipfile import is_zipfile

from chromie.config import Config
from chromie.webstore import GoogleWebStore, GoogleWebStoreError
from chromie.auth import AuthenticationError
from chromie.commands.messages import Settings, Update


def get_latest_version(fp):
    archives = [fn for fn in os.listdir(fp) if is_zipfile(os.path.join(fp, fn))]

    archives.sort(reverse=True)
    return os.path.join(fp, archives[0])


def update(args):
    root = os.path.abspath(args.filepath)

    dist = os.path.join(root, "dist")
    dot_chromie = os.path.join(root, ".chromie")

    if not os.path.isdir(dot_chromie):
        raise SystemExit(Settings.MISSING)

    archive = get_latest_version(dist)

    config_file = Config.from_file(os.path.join(dot_chromie, "settings.json"))

    try:
        with GoogleWebStore.session(
            config_file.data.get("email"), credentials=config_file.data
        ) as session:
            try:
                extension_id = session.update(config_file.data["extension_id"], archive)
                print(Update.SUCCESS)
            except GoogleWebStoreError as e:
                print(e)
    except AuthenticationError:
        print(Settings.INVALID)
