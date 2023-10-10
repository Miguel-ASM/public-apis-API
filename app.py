import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api as RestfulApi
from api import ApiResource


# Create flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping':True}


# CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Postgres config
from db import db
import models
migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db)

@app.get('/api/ping')
def ping():
    return "digame(lon)",200

# Api endpoint for performing search and obtaining a json response
api = RestfulApi(app)
api.add_resource(ApiResource,'/api/search')