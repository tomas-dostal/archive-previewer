import os
import json
from flask_sqlalchemy import SQLAlchemy
from database import db
from jsonmerge import merge

basedir = os.path.abspath(os.path.dirname(__file__))


class Archive(db.Model):
    __tablename__ = "archive"

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String())

    # Intentionally used JSON string apart of 1:N, because in case / will be called often
    # then I'd need to perform quite heavy DB query (a lot of joins) and then transform the result
    # to JSON. Also, the uploaded archive remains, no further changes are allowed.
    # Therefore, just a JSON string would be served.

    # Please note, that this solution is intended to be as minimal as possible

    content_json = db.Column(db.Text())

    def json(self):
        return json.dumps({"id": self.id, "file": self.file_name, **json.loads(self.content_json)})

    def __repr__(self):
        return "<Archive id: {}>".format(self.id)
