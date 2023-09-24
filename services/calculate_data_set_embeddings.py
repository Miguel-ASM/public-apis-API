import  json
from pathlib import Path
import openai

openai.api_key = "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"

data_dir = Path(__file__).parent.parent.joinpath('data')
input_file_path = data_dir.joinpath('apis.json')
output_file_path = data_dir.joinpath('apis-with-embeddings.json')

with open(input_file_path) as f:
  apis_list = json.load(f)

texts = [ data.get('description') for data in apis_list ]

embeddings_response = openai.Embedding.create(
  model="text-embedding-ada-002",
  input=texts
)

embeddings_iter = (
    item.get('embedding')
    for item in embeddings_response.get('data',[])
)

apis_list_with_embeddings = [
  api | {'embedding': embedding }
  for api, embedding in zip(apis_list,embeddings_iter)
]

with open(output_file_path,'w') as f:
  json.dump(apis_list_with_embeddings,f)
