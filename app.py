from flask import Flask, request, render_template
from services.elasticsearch_client import elastic
from sentence_transformers import SentenceTransformer


# Elastic search client
es = elastic.es

# Transformer for obtaining embeddings from text input
model = SentenceTransformer('all-MiniLM-L6-v2')
def getembedding(text):
    return list( model.encode(text) )


app = Flask(__name__,static_folder='public')


@app.get('/api/search')
def search_apis():
    query = request.args.get('query')
    embedding = getembedding(query)
    es_response = es.search(
        index=elastic.index,
        query= {
            "script_score": {
                "query": { "match_all": {} },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": embedding}
                }
            }
        },
        source_excludes=['embedding']
    )
    search_results = [doc.get('_source') for doc in es_response.get('hits').get('hits')]
    
    return {'results': search_results}


@app.get('/')
def home():
    examples = ['videogames and comics', 'movies or series', 'natural sciences']
    query = request.args.get('query')
    if query is None:
        return render_template('index.html',context={'results':[]},examples = examples)

    embedding = getembedding(query)
    es_response = es.search(
        index=elastic.index,
        query= {
            "script_score": {
                "query": { "match_all": {} },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": embedding}
                }
            }
        },
        source_excludes=['embedding']
    )
    search_results = [doc.get('_source') for doc in es_response.get('hits').get('hits')]
    print(search_results)
    return render_template('index.html',results = search_results, examples = examples)