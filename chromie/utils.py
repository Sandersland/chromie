from enum import Enum
import os
import ntpath
import json


class Paths(Enum):
    gitignore = ".gitignore"
    zipignore = ".zipignore"
    dist = "dist/"
    web_store = "dist/web store/"
    src = "src/"
    images = "src/images"
    manifest = "src/manifest.json"


class ChromiePathFinder(dict):
    def __init__(self, path=os.getcwd(), name=None, paths=Paths):
        if not name:
            path, name = os.path.split(path)
        self.path = path
        self.name = name
        self.paths = paths

    @property
    def root(self):
        return os.path.join(self.path, self.name)

    def __call__(self, name):
        dir = Paths[name].value
        if not dir:
            raise ValueError(f"No path with the name {name} exists")
        return os.path.abspath(os.path.join(self.root, dir))

    def exists(self, name=""):
        path = os.path.abspath(os.path.join(self.root, name))
        return os.path.exists(path)


class ManifestFile:
    def __init__(self, path, data):
        self.path = path
        self.data = data

    @classmethod
    def from_file(cls, path):
        with open(path, "r") as f:
            data = json.load(f)
        return cls(path, data)

    def write(self, data=None):
        data = self.data if not data else data
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)
        return True

    def increment_version(self, increment_name):

        current_version = self.data["version"]

        major, minor, patch = current_version.split(".")

        if increment_name == "major":
            major = str(int(major) + 1)

        elif increment_name == "minor":
            minor = str(int(minor) + 1)

        elif increment_name == "patch":
            patch = str(int(patch) + 1)

        new_version = ".".join((major, minor, patch))

        self.data["version"] = current_version.replace(current_version, new_version)

        self.write()
        return new_version

    def set_version(self, version):
        current_version = self.data["version"]

        self.data["version"] = current_version.replace(current_version, version)
        self.write()
        return version
