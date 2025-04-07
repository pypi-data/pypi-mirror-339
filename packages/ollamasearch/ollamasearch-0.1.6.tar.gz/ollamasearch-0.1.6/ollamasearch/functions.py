# functions.py
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model globally
embedding_model = SentenceTransformer('manu/bge-m3-custom-fr')

def getembedding(text_or_texts):
    """
    Returns embeddings for the input text or list of texts using SentenceTransformer.
    If a single string is provided, it is wrapped in a list.
    """
    if isinstance(text_or_texts, str):
        text_or_texts = [text_or_texts]
    embeddings = embedding_model.encode(text_or_texts, convert_to_numpy=True)
    return embeddings
