from flask import request, session
from marshmallow import ValidationError

from config import app
from domains.authentication.service import login_required
from domains.pagination.model import PaginationSchema
from domains.results.model import ResultSchema
from domains.results.service import ResultsService

results_service = ResultsService()


@app.route("/api/v1/results")
@login_required
def get_results():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 100))
    results = results_service.get_results(page, limit)
    result_schema = ResultSchema(many=True)
    pagination_schema = PaginationSchema()
    return {"results": result_schema.dump(results.items),
            "pagination": pagination_schema.dump(results)}


@app.route("/api/v1/results", methods=["POST"])
def create_result():
    json_data = request.get_json()
    result_schema = ResultSchema()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    try:
        data = result_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422

    result = results_service.create_result(data)
    return result_schema.dump(result)
