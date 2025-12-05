from api import ma
from marshmallow import fields

class MovieSchema(ma.Schema):
    _id = fields.Str()
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    year = fields.Int(required=True)
    duration = fields.Int(required=True)

    