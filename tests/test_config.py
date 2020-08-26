import json
import tempfile
import unittest
from unittest.mock import patch, mock_open

from chromie.config import Config


class TestConfig(unittest.TestCase):
    @patch("chromie.config.os.path.isfile", return_value=True)
    def test_from_file_exists(self, mock_isfile):
        data = '{"hello":"there"}'
        m = mock_open(read_data=data)
        path = "./this/is/a/test"
        with patch("chromie.config.open", m):
            result = Config.from_file(path)
            m.assert_called_once_with(path, "r")
            self.assertEqual(result.data, json.loads(data))

    def test_from_file_does_not_exist(self):
        pass


if __name__ == "__main__":
    unittest.main()
