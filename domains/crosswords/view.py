from flask import request, session
from marshmallow import ValidationError

from config import app
from domains.authentication.service import login_required
from domains.crosswords.service import CrossWordService
from domains.pagination.model import PaginationSchema

crossword_service = CrossWordService()


@app.route("/api/v1/crosswords")
@login_required
def get_crosswords():
    pass
    # page = int(request.args.get("page", 1))
    # limit = int(request.args.get("limit", 100))
    # results = crossword_service.get_crosswords(page, limit)
    # result_schema = ResultSchema(many=True)
    # pagination_schema = PaginationSchema()
    # return {
    #     "results": result_schema.dump(results.items),
    #     "pagination": pagination_schema.dump(results),
    # }


@app.route("/api/v1/load_crosswords", methods=["GET"])
def load_crosswords():
    crossword_service.load_crosswords()

    return {"status": "success"}
