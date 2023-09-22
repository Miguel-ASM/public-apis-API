from flask_restful import Resource, request
from services.search_apis import search

class ApiResource(Resource):
  def get(self):

    query = request.args.get('query')
    page = int(request.args.get('page',1))

    if query is None:
      return {
        'error': 'query must not be empty. Please provide it by the queryparam "?query=<query>"'
      }, 400
    
    return search(query,page), 200
