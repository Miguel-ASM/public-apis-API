from flask_restful import Resource, request
from services.get_categories import getcategories


class CategoriesResource(Resource):
  def get(self):
    page = int(request.args.get('page') or 1)
    return getcategories(page), 200
