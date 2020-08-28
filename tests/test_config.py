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

    @patch("chromie.config.os.path.isfile", return_value=False)
    def test_from_file_does_not_exist(self, mock_isfile):
        m = mock_open()
        path = "./this/is/a/test"
        with patch("chromie.config.open", m, create=True):
            result = Config.from_file(path)
            m.assert_called_once_with(path, "w")
            handle = m()
            handle.write.assert_called_once_with("")
            self.assertEqual(result.data, {})

    @patch("chromie.config.os.path.isfile", return_value=True)
    def test_set_new_values(self, mock_file):
        m = mock_open()
        path = "./this/is/a/test.json"
        with patch("chromie.config.open", m):
            config = Config.from_file(path)

        with patch("chromie.config.open", m):
            config.set_values(hello="there")
            self.assertEqual(config.data, {"hello": "there"})

    @patch("chromie.config.os.path.isfile", return_value=True)
    def test_update_values(self, mock_file):
        m = mock_open(read_data=json.dumps({"hello": "there"}))
        path = "./this/is/a/test.json"
        with patch("chromie.config.open", m):
            config = Config.from_file(path)

        with patch("chromie.config.open", m):
            config.set_values(hi="again")
            test_case = {"hello": "there", "hi": "again"}
            self.assertEqual(config.data, test_case)


if __name__ == "__main__":
    unittest.main()
