import os

from chromie.config import Config


def config(args):
    filepath = os.path.abspath(args.filepath)
    dot_chromie = os.path.join(filepath, ".chromie")

    if not os.path.isdir(dot_chromie):
        os.mkdir(dot_chromie)

    config_file = Config.from_file(os.path.join(filepath, ".chromie/settings.json"))
    data = {args.name: args.value}
    config_file.set_values(**data)

