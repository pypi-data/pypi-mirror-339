# search.py
import requests
import json
from .simplesearch import SimpleSearch
from . import importdocs
from .functions import getembedding

def perform_search(query, model, api_key, top_k=2):
    """
    For queries starting with '/', this pipeline:
      1. Uses the user query directly to obtain search context,
      2. Uses the raw context (without summarization) and stores it in the FAISS RAG index,
      3. Constructs a final prompt that includes both the original query and the context,
      4. Sends the final prompt to Ollama for generation with a streaming response.
      
    For queries without '/', it falls back to the standard RAG pipeline with streaming.
    """
    ollama_url = "http://localhost:11434/api/chat"
    headers = {"Content-Type": "application/json"}

    if query.startswith('/'):
        searcher = SimpleSearch(
            cloud_service_url="https://edneorfuvixmugzdyuhr.supabase.co/functions/v1/ratelimit",
            ollama_url="http://localhost:11434",
            current_model=model,
            api_key=api_key
        )
        supporting_info = searcher.process_query(query)
        user_query = query[1:].strip()

        # Format the content FROM supporting_info for the improved prompt
        context_from_info = (
            f"Relevant Content:\n{supporting_info.get('full_text', 'N/A')}\n\n"
            f"---\nSource URLs:\n{supporting_info.get('urls', 'N/A')}"
        )

        # Use the improved prompt structure WITH the formatted context
        final_prompt = (
            f"You are an assistant answering a user's query based *only* on the following context.\n\n"
            f"=== Context Start ===\n\n"
            f"{context_from_info}"  # Content derived from supporting_info
            f"=== Context End ===\n\n"
            f"Based *only* on the context provided above, answer the following user query:\n"
            f'User Query: "{user_query}"'
        )
        messages = [{"role": "user", "content": final_prompt}]
    else:
        # Standard RAG pipeline for queries without '/'.
        query_embed = getembedding(query)
        if query_embed.ndim == 1:
            query_embed = query_embed.reshape(1, -1)
        indices, distances = importdocs.search_index(query, model, top_k=2)
        docs = [importdocs.doc_store[i] for i in indices if i in importdocs.doc_store]
        if docs:
            # Use improved prompt structure for non-'/' queries
            relateddocs = "\n\n---\n\n".join(docs) # Add separator between chunks
            prompt = (
                f"You are an assistant answering a user's query based *only* on the following context.\n\n"
                f"=== Context Start ===\n\n"
                f"{relateddocs}"
                f"=== Context End ===\n\n"
                f"Based *only* on the context provided above, answer the following user query:\n"
                f'User Query: "{query}"'
            )
        else:
            prompt = query
        messages = [{"role": "user", "content": prompt}]

    payload = {
        "model": model,
        "messages": messages,
        "stream": True
    }

    try:
        # Using stream=True to enable streaming of the final response.
        with requests.post(ollama_url, json=payload, headers=headers, stream=True) as response:
            response.raise_for_status()
            full_response = ""
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    content = chunk.get("message", {}).get("content", "")
                    print(content, end="", flush=True)
                    full_response += content
            print()  # Ensure a newline after streaming is complete.
            return full_response
    except Exception as e:
        print(f"Error in generation: {e}")
        return ""
