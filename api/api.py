from flask_restful import Resource
from models import Api
from sqlalchemy import select

class ApiResource(Resource):
  def get(self):
    apis = Api.query.all()
    print([api.name for api in apis])
    # return [dict(user) for user in Api.query.all()]
    return 200
