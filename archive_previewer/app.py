import os
from zipfile import ZipFile, BadZipFile

from flask import request, jsonify, Flask

import archive_previewer.config
from archive_previewer.database import db
from archive_previewer.models import Archive, File
from archive_previewer.schema import ArchiveSchema

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = set("zip")
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(basedir, "data.sqlite"))

app = Flask(__name__)
app.config.from_object("archive_previewer.config.DevelopmentConfig")  # os.environ.get('FLASK_ENV') or
db.init_app(app)


@app.route("/", methods=["POST"])
def upload_file():
    if not request.files:
        return jsonify(error=400, text="No files attached"), 400
    if len(request.files) > 1:
        return jsonify(error=400, text="Multiple files attached. Please send separately"), 400

    # it might be useful to store files directly to the local drive and write the by chunks,
    # especially if file is large. Currently file size is limited to 2MB

    file = next(iter(request.files.listvalues()))[0]

    if file.filename != "":
        file_ext = os.path.splitext(file.filename)[1]
        if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
            return (
                jsonify(
                    error=400,
                    text="Invalid format. Allowed formats: {allowed}".format(
                        allowed=archive_previewer.config.Config.UPLOAD_EXTENSIONS
                    ),
                ),
                400,
            )

    archive = Archive(name=file.filename)
    try:
        with ZipFile(file=file) as zip:
            content = [File(path=file.filename, size=file.file_size) for file in zip.filelist]
            archive.files.extend(content)
            db.session.add_all(content)
            db.session.add(archive)
            db.session.commit()

            return ArchiveSchema().dump(archive)
    except BadZipFile:
        return jsonify(error=422, text="Unable to process the file"), 422


@app.route("/", methods=["GET"])
def list_all_files():
    return jsonify(ArchiveSchema().dump(Archive.query.all(), many=True))


@app.route("/archive/<archive_id>", methods=["GET"])
def get_page(archive_id):
    result = db.session.query(Archive).filter(Archive.id == archive_id).first()
    if not result:
        return jsonify(error=404, text="Archive not found"), 404
    return jsonify(result)


if __name__ == "__main__":
    db.create_all()
    app.run()


@app.before_first_request
def create_tables():
    db.create_all()
