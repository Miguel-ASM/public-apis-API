from sqlalchemy import select,func

from db import db
from models import Api
from services.embedding import getembedding

MAX_COSINE_DISTANCE = 0.22
MAX_RESULTS_PER_PAGE = 10

def search(query,page = 1):
  if query is None: raise ValueError('A query must be provided.')
  embedding = getembedding(query)
  results_query = select(
      Api.name,
      Api.category,
      Api.url,
      Api.description,
      Api.cors,
      Api.auth,
      Api.https,
  ).where( 
      Api.embedding.cosine_distance( embedding ) < MAX_COSINE_DISTANCE 
  ).order_by( 
    Api.embedding.cosine_distance( embedding )
  ).offset(
      MAX_RESULTS_PER_PAGE * ( page - 1 )
  ).limit( MAX_RESULTS_PER_PAGE )

  total_hits_count_query = select( func.count() ) \
    .select_from(Api) \
    .where( 
      Api.embedding.cosine_distance( embedding ) < MAX_COSINE_DISTANCE 
    )
  
  total_hits = db.session.scalar(total_hits_count_query)

  result_rows = db.session.execute(results_query)
  apis_data = [ x._asdict() for x in result_rows ]

  return {
      'total_hits': total_hits ,
      'page_size': MAX_RESULTS_PER_PAGE,
      'page': page,
      'results': apis_data
  }
