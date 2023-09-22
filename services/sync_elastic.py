from pathlib import Path
from sqlalchemy import create_engine, insert
import os
from models import Api
import json
import numpy as np

engine = create_engine(os.environ.get("DB_URL"))

data_dir = Path(__file__).parent.parent.joinpath('data')
input_file_path = data_dir.joinpath('apis-with-embeddings.json')

with open(input_file_path) as f:
  docs = json.load(f)
  docs = [{**x,'embedding':np.array(x.get('embedding'))} for x in docs ]

with engine.connect() as connection:
  with connection.begin():
    result = connection.execute(insert(Api),docs)