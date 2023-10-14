from flask_restful import Resource, request
from sqlalchemy import select, func, cte

from db import db
from models import Api

MAX_RESULTS_PER_PAGE = 10

categories_with_counts = select(
  Api.category.label('category'),
  func.count().label('count')
).group_by(
  Api.category
).cte("categories_with_counts")

categories_query = select(
  categories_with_counts
).order_by(
  categories_with_counts.c.category
)


class CategoriesResource(Resource):
  def get(self):
    page = int(request.args.get('page') or 1)
    paginated_categories_query = categories_query.offset(
        MAX_RESULTS_PER_PAGE * ( page - 1 )
    ).limit( MAX_RESULTS_PER_PAGE )
    rows = db.session.execute(paginated_categories_query).fetchall()
    return {'categories':[ x._asdict() for x in rows]}, 200
