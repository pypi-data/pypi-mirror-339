# importdocs.py
import numpy as np
import faiss
from .functions import getembedding
import re

# Global FAISS index and document store
faiss_index = None
doc_store = {}  # Mapping: integer index -> document text

def get_index(d):
    """
    Initialize the FAISS index without quantization.
    'd' is the dimension of the embeddings.
    """
    global faiss_index
    if faiss_index is None:
        faiss_index = faiss.IndexFlatL2(d)  # Plain L2 index (no quantization)
    return faiss_index

def chunk_text_sentence(text, target_words=900, overlap_words=100):
    """
    Splits text into chunks based on sentence boundaries.
    Combines sentences until a target word count is reached.
    Uses an overlap of a given number of words between chunks.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []
    current_count = 0
    for sentence in sentences:
        sentence_word_count = len(sentence.split())
        if current_count + sentence_word_count <= target_words:
            current_chunk.append(sentence)
            current_count += sentence_word_count
        else:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            # Create overlap: take the last `overlap_words` from the current chunk
            if overlap_words > 0 and current_chunk:
                words = " ".join(current_chunk).split()
                overlap = words[-overlap_words:] if len(words) >= overlap_words else words
                current_chunk = [" ".join(overlap)]
                current_count = len(overlap)
            else:
                current_chunk = []
                current_count = 0
            current_chunk.append(sentence)
            current_count += sentence_word_count
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def chunk_text_word(text, target_words=900, overlap_words=100):
    """
    Splits text into chunks using a simple sliding window at the word level.
    This does not take sentence boundaries into account.
    """
    words = text.split()
    if len(words) <= target_words:
        return [text]
    chunks = []
    start = 0
    while start < len(words):
        end = start + target_words
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end >= len(words):
            break
        start = end - overlap_words  # Overlap for continuity
    return chunks

def update_collection_with_text(doc_name, text, chunking_strategy="sentence", target_words=900, overlap_words=100):
    """
    Embeds the provided text by first splitting it into chunks.
    Depending on the chosen strategy ('sentence' or 'word'), it splits the text accordingly.
    Then, it embeds each chunk and adds it to the FAISS index, storing each chunk in the doc_store.
    """
    global doc_store
    if chunking_strategy == "word":
        chunks = chunk_text_word(text, target_words, overlap_words)
    else:
        chunks = chunk_text_sentence(text, target_words, overlap_words)
    
    d = None
    index = None
    start_id = len(doc_store)
    for chunk in chunks:
        embeds = getembedding(chunk)
        if embeds.ndim == 1:
            embeds = embeds.reshape(1, -1)
        if d is None:
            d = embeds.shape[1]
            index = get_index(d)
        index.add(embeds)
        doc_store[start_id] = chunk
        start_id += 1
    print(f"Collection updated with document ")

def search_index(query, model, top_k=5):
    """
    Perform a semantic search over the FAISS index.
    Returns a tuple of (indices, distances).
    """
    q_embed = getembedding(query)
    if q_embed.ndim == 1:
        q_embed = q_embed.reshape(1, -1)
    if faiss_index is None or faiss_index.ntotal == 0:
        return [], []
    distances, indices = faiss_index.search(q_embed, top_k)
    return indices[0], distances[0]

def reset_collection():
    """
    Reset the FAISS-based RAG database.
    """
    global faiss_index, doc_store
    faiss_index = None
    doc_store = {}
