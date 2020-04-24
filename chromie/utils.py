from enum import Enum
import os
import ntpath


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
