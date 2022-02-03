# Archive previewer

The task is to implement an "Archive previewer" HTTP JSON API in python using [flask](https://flask.palletsprojects.com/en/2.0.x/) web framework. That API accepts a ZIP file, processes it on the server, and returns results of processing (list of files inside with their sizes) to the user in JSON format. All processing results are saved to the SQLite database. Repository with the project should be hosted on the https://github.com/ and Github Actions should be used for checking code style with [pylint](https://www.pylint.org/) and running tests.

## API Description

The API should accept 2 requests. One request to upload a file and see its uploading results and the second one to see all previously uploaded files. Every uploaded file should be processed only once (and then discarded), data about the file should be saved to an SQLite database. [SQLAlchemy](https://www.sqlalchemy.org/) should be used as an ORM for accessing data.

1. `GET /`
   This endpoint returns a list of all files that were previously uploaded to the service.

   Example output:

   ```json
   [
     {
       "id": 1,
       "file": "test.zip",
       "content": [
         { "path": "a.txt", "size": 3032 },
         { "path": "vacation/summer.jpg", "size": 300720 }
       ]
     },
     {
       "id": 2,
       "file": "test2.zip",
       "content": [{ "path": "let/it/be.exe", "size": 487348 }]
     }
   ]
   ```

2. Result page `POST /`

   This endpoint accepts one file as a request body and returns the content of the file. By the end of request processing, the file should not be saved on the server.

   Example request:

   ```
   curl --request POST -F "file=@/path/to/file.zip" http://localhost:8000
   ```

   Example response:

   ```json
   {
     "id": 3,
     "file": "file.zip",
     "content": [{ "path": "something.docx", "size": 754678 }]
   }
   ```

## Tests and CI

Source code should be stored in a public repository on https://github.com/ or in a private one shared with user `https://github.com/kumekay`. It's recommended to not only push the final code to the repo, but also make commits during the process.

### Optional

Project repo should contain `.github/workflows` directory with a workflow, that defines 2 jobs: `test` and `lint` .

During the linting stage, the codebase should be checked using pylint (with any set of rules). Tests should be written using [pytest](https://docs.pytest.org/en/6.2.x/) . There should be at least one unit test for a function that processes a zip archive and one integration test that uploads a known zip file and checks the output of the `POST /` endpoint.

## Useful links

- https://docs.python.org/3.8/library/zipfile.html#zipfile.ZipFile.infolist