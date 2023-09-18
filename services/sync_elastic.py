import json
from pathlib import Path
from services.elasticsearch_client import elastic

data_dir = Path(__file__).parent.parent.joinpath('data')
input_file_path = data_dir.joinpath('apis-with-embeddings.json')

with open(input_file_path) as f:
  docs = json.load(f)

elastic.resetindex()
es = elastic.es

for doc in docs:
  es.index(index=elastic.index, document=doc)
