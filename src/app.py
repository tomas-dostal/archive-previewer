import os
import json
from zipfile import ZipFile

from flask import request, jsonify, Flask
from database import db
from models import Archive

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = set(["zip"])
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(basedir, "data.sqlite"))

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")  # os.environ.get('FLASK_ENV') or


db.init_app(app)


@app.route("/", methods=["POST"])
def upload_file():
    if not request.files:
        return jsonify(error=400, text="No files attached"), 400
    if len(request.files) > 1:
        return jsonify(error=400, text="Multiple files attached. Please send separately"), 400

    file = request.files.getlist("file")[0]
    with ZipFile(file=file) as zip:
        res = [{"path": file.filename, "size": file.file_size} for file in zip.filelist]

        archive = Archive(file_name=file.filename, content_json=json.dumps({"content": res}))
        db.session.add(archive)
        db.session.commit()

        return archive.json()


if __name__ == "__main__":
    db.create_all()
    app.run()


@app.before_first_request
def create_tables():
    db.create_all()
