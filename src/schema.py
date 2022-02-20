from marshmallow import Schema, fields


class FileSchema(Schema):
    class Meta:
        ordered = True

    path = fields.String()
    size = fields.Integer()


class ArchiveSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer()
    name = fields.String()
    content = fields.Nested(FileSchema, many=True, attribute="files")
