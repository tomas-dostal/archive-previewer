import io
import unittest
from pathlib import Path

from archive_previewer.app import app


class BasicTest(unittest.TestCase):
    def test_base_route(self):
        # app = Flask(__name__)
        client = app.test_client()
        url = "/"
        response = client.get(url)
        assert response.status_code == 200


class UploadedFileProcessingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()
        self.root = "/"

    def test_no_zip_file_sent(self, requests=None):
        self.assertEqual(self.client.post(self.root).status_code, 400)

    def test_multiple_zip_files_sent(self):
        files = {
            "file_1": open(Path(__file__).parent / "resources/readable_three_files.zip", "rb"),
            "file_2": open(Path(__file__).parent / "resources/readable_three_files.zip", "rb"),
        }
        self.assertEqual(self.client.post(self.root, data=files).status_code, 400)

    def test_corrupted_zip_file(self):
        file_name = "iamnotazipfile.zip"
        data = {"file": (io.BytesIO(b"some initial text data"), file_name)}
        response = self.client.post(self.root, data=data)
        assert response.status_code == 422

    def test_suffix_of_uploaded_file_is_not_zip(self):
        files = {
            "file_1": open(Path(__file__).parent / "resources/zip_file_without_zip_suffix.txt", "rb"),
        }
        response = self.client.post(self.root, data=files)
        self.assertEqual(response.status_code, 400)
        print(response.json)
        self.assertTrue("Invalid format" in response.json["text"])

    def test_empty_zip_file(self):
        files = {"file_1": open(Path(__file__).parent / "resources/empty.zip", "rb")}
        response = self.client.post(self.root, data=files)
        # b'{\n  "id": 4, \n  "name": "resources/empty.zip", \n  "content": []\n}\n'
        self.assertEqual(response.status_code, 200)

    def test_encrypted_zip_file(self):
        # Listing of files even encrypted is OK -- https://kb.corel.com/en/125899
        path = Path(__file__).parent / "resources/encrypted.zip"
        files = {
            "file_1": open(path, "rb"),
        }
        response = self.client.post(self.root, data=files)
        print(response.data)
        print(response)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
