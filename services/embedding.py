import os
import openai

openai.api_key = os.environ.get('OPENAI_API_KEY')
EMBEDDING_MODEL = 'text-embedding-ada-002'

def getembedding(text):
    embeddings_response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    embedding = embeddings_response.get('data')[0].get('embedding')
    return embedding

def getembeddings(texts_array,as_iter=True):
    embeddings_response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=texts_array
    )
    embeddings_iter = (
        item.get('embedding')
        for item in embeddings_response.get('data',[])
    )
    if as_iter: return embeddings_iter
    return list(embeddings_iter)