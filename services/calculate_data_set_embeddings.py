import  json
from sentence_transformers import SentenceTransformer
from pathlib import Path


data_dir = Path(__file__).parent.parent.joinpath('data')
input_file_path = data_dir.joinpath('apis.json')
output_file_path = data_dir.joinpath('apis-with-embeddings.json')

model = SentenceTransformer('all-MiniLM-L6-v2')

with open(input_file_path) as f:
  apis_list = json.load(f)

embeddings = model.encode([api.get('description') for api in apis_list])

apis_list_with_embeddings = [
  api | {'embedding':list(embedding.astype(float))}
  for api, embedding in zip(apis_list,embeddings)
]

with open(output_file_path,'w') as f:
  json.dump(apis_list_with_embeddings,f)
