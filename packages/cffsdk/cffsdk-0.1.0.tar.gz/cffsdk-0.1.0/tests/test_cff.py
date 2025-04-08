import unittest
from unittest.mock import patch
from cffsdk import cffsdk

class TestCFFClient(unittest.TestCase):
    def setUp(self):
        self.client = cffsdk(base_url="http://127.0.0.1:8000")

    @patch("requests.get")
    def test_get_root(self, mock_get):
        mock_get.return_value.json.return_value = {"message": "Hello"}
        response = self.client.get_root()
        self.assertEqual(response, {"message": "Hello"})
        mock_get.assert_called_once_with("http://127.0.0.1:8000/")

    @patch("requests.get")
    def test_get_about(self, mock_get):
        mock_get.return_value.json.return_value = {"message": "This is the about page."}
        response = self.client.get_about()
        self.assertEqual(response, {"message": "This is the about page."})
        mock_get.assert_called_once_with("http://127.0.0.1:8000/about")

    @patch("requests.post")
    def test_post_message(self, mock_post):
        mock_post.return_value.json.return_value = {"message": {"msg_id": 1, "msg_name": "example_message"}}
        response = self.client.post_message("example_message")
        self.assertEqual(response, {"message": {"msg_id": 1, "msg_name": "example_message"}})
        mock_post.assert_called_once_with("http://127.0.0.1:8000/messages/example_message")

if __name__ == "__main__":
    unittest.main()