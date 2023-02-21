from flask import request
from marshmallow import ValidationError

from config import app
from domains.authentication.guards import authorization_guard
from domains.crosswords.model import CrosswordQuerySchema, CrosswordSchema
from domains.crosswords.service import CrossWordService
from domains.pagination.model import PaginationSchema

crossword_service = CrossWordService()


@app.route("/api/v1/crosswords")
@authorization_guard
def get_crosswords():
    try:
        query_schema = CrosswordQuerySchema()
        data = query_schema.load(request.args)
    except ValidationError as err:
        return err.messages, 422

    page = int(data.get("page", 1))
    limit = int(data.get("limit", 100))
    dow = data.get("dow")
    col_size = data.get("col_size")
    row_size = data.get("row_size")

    results = crossword_service.get_crosswords(page, limit, dow, col_size, row_size)
    schema = CrosswordSchema(many=True)
    pagination_schema = PaginationSchema()
    return {
        "results": schema.dump(results.items),
        "pagination": pagination_schema.dump(results),
    }


@app.route("/api/v1/load_crosswords", methods=["GET"])
def load_crosswords():
    crossword_service.load_crosswords()

    return {"status": "success"}
