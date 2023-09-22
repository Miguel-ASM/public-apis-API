
from sentence_transformers import SentenceTransformer

# Transformer for obtaining embeddings from text input
model = SentenceTransformer('all-MiniLM-L6-v2')
def getembedding(text):
    return list( model.encode(text) )