from sqlalchemy import select, func, distinct

from db import db
from models import Api

MAX_RESULTS_PER_PAGE = 10


def getcategoriescount():
  categories_count_query = select(func.count(distinct(Api.category)))
  return db.session.execute(categories_count_query).scalar()

def getcategories(page=1):
  categories_with_counts = select(
    Api.category.label('category'),
    func.count().label('count')
  ).group_by(
    Api.category
  ).cte("categories_with_counts")

  paginated_categories_query = select(
    categories_with_counts
  ).order_by(
    categories_with_counts.c.category
  ).offset(
      MAX_RESULTS_PER_PAGE * ( page - 1 )
  ).limit( MAX_RESULTS_PER_PAGE )

  rows = db.session.execute(paginated_categories_query).fetchall()
  categories_count = getcategoriescount()
  
  return {
    'categories_count': categories_count,
    'page': page,
    'page_size': MAX_RESULTS_PER_PAGE,
    'categories':[ x._asdict() for x in rows]
  }