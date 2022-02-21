import os
from zipfile import ZipFile, BadZipFile

from flask import request, jsonify, Flask
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

    file = next(iter(request.files.listvalues()))[0]
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
    return jsonify(Archive.query.all())


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
