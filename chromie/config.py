import json
import os
from codecs import escape_decode
from json.decoder import JSONDecodeError


class Config:
    def __init__(self, fp, data=None):
        self.fp = fp
        self._data = data

    @classmethod
    def from_file(self, fp):
        if not os.path.isfile(fp):
            with open(fp, "w") as f:
                f.write("")
            return Config(fp, {})

        file = open(fp, "r")
        try:
            data = json.load(file)
            return Config(fp, data)
        except JSONDecodeError:
            return Config(fp, {})

        finally:
            file.close()

    @property
    def data(self):
        return self._data if self._data else {}

    def set_values(self, **kwargs):
        for k, v in kwargs.items():
            if not v:
                del self._data[k]
                continue
            self._data[k] = v.encode("utf-8").decode("unicode_escape")

        with open(self.fp, "w") as f:
            json.dump(self._data, f, indent=2)

    def __str__(self):
        return json.dumps(self.data, indent=2)
