import os
import openai

openai.api_key = os.environ.get('OPENAI_API_KEY')

def getembedding(text):
    embeddings_response = openai.Embedding.create(
    model="text-embedding-ada-002",
    input=text
    )
    embedding = embeddings_response.get('data')[0].get('embedding')
    return embedding