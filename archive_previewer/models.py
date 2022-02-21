import os
from archive_previewer.database import db

basedir = os.path.abspath(os.path.dirname(__file__))


class Archive(db.Model):
    __tablename__ = "archive"

    id = db.Column(db.Integer, primary_key=True)
    # Please note, that this solution is intended to be as minimal as possible

    name = db.Column(db.String())

    # folder structure is kept by the file path
    files = db.relationship("File", lazy="joined")  # want to optimize number of queries

    def __repr__(self):
        return "<Archive id: {id}>".format(id=self.id)


class File(db.Model):
    __tablename__ = "file"

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String())
    size = db.Column(db.Integer())
    archive_id = db.Column(db.Integer, db.ForeignKey("archive.id"))

    def __repr__(self):
        return "<File id: {id}, path: {path}>".format(id=self.id, path=self.path)
