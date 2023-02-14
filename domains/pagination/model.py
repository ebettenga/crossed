from marshmallow import Schema, fields


class PaginationSchema(Schema):
    total = fields.Int()
    pages = fields.Int()
    per_page = fields.Int()
    has_next = fields.Bool()
    has_prev = fields.Bool()
    next_num = fields.Int()
    prev_num = fields.Int()
