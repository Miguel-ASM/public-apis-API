import os

from flask import Flask, request, render_template
from flask_migrate import Migrate
from flask_restful import Api as RestfulApi
from api import ApiResource

from services.search_apis import search

# Create flask app
app = Flask(__name__,static_folder='public')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping':True}


# Postgres config
from db import db
import models
migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db)


# Endpoint for a home page
@app.get('/')
def home():
    examples = ['videogames and comics', 'movies or series', 'natural sciences']
    query = request.args.get('query')
    page = int(request.args.get('page') or 1)

    if query is None:
        return render_template('index.html',context={'results':[]},examples = examples)
    
    search_results_data = search(query,page)
    results = search_results_data.get('results')
    page_size = search_results_data.get('page_size')
    total_hits = search_results_data.get('total_hits')

    return render_template('index.html', examples = examples, **search_results_data)


@app.get('/api/ping')
def ping():
    return "digame(lon)",200

# Api endpoint for performing search and obtaining a json response
api = RestfulApi(app)
api.add_resource(ApiResource,'/api/search')