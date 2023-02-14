from flask_sqlalchemy.pagination import Pagination

from config import db
from domains.results.model import Result, ResultQueryClient


class ResultsService:

    def create_result(self, data: dict):
        # Create new quote
        result = Result(url=data.get("url"), result_all=data.get("result_all"),
                        result_no_stop_words=data.get("result_no_stop_words"))
        db.session.add(result)
        db.session.commit()

        return result

    def get_results(self, page: int, limit: int) -> Pagination:
        results: ResultQueryClient = Result.query

        results_pagination = results.paginate(page=page, per_page=limit)
        return results_pagination
