import unittest
from archive_previewer.app import app


class BasicTest(unittest.TestCase):
    def test_base_route(self):
        client = app.test_client()
        url = "/"
        response = client.get(url)
        assert response.status_code == 200
