# simplesearch.py
import requests
import json
import re
from . import importdocs  # For storing the search context in the FAISS RAG index

class SimpleSearch:
    def __init__(self, cloud_service_url, ollama_url, current_model, api_key):
        self.cloud_service_url = cloud_service_url
        self.ollama_url = ollama_url
        self.current_model = current_model
        self.api_key = api_key  # Stored for use with web search
        self.search_url = "https://edneorfuvixmugzdyuhr.supabase.co/functions/v1/ratelimit"

    def call_ollama(self, prompt, stream=False):
        payload = {
            "model": self.current_model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": stream
        }
        headers = {
            "Content-Type": "application/json"
        }
        try:
            if stream:
                with requests.post(
                    self.ollama_url,
                    json=payload,
                    headers=headers,
                    stream=stream
                ) as response:
                    response.raise_for_status()
                    full_response = ""
                    for line in response.iter_lines():
                        if line:
                            chunk = json.loads(line)
                            content = chunk.get("message", {}).get("content", "")
                            print(content, end="", flush=True)
                            full_response += content
                    print()
                    return full_response
            else:
                response = requests.post(
                    self.ollama_url,
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                result = response.json()
                return result.get("message", {}).get("content", "")
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return ""

    def get_search_context(self, search_query):
        """
        Performs a search request and returns a dictionary containing:
          - "full_text": the full content from all results (for storage), and
          - "urls": a concatenation of URLs from the search results (for display).
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        try:
            response = requests.post(
                self.search_url,
                json={"query": search_query},
                headers=headers
            )
            response.raise_for_status()
            result = response.json()
            if not result.get("success"):
                return {"full_text": "No relevant information found.", "urls": "No relevant information found."}
            contexts = result.get('data', [])
            if not contexts:
                return {"full_text": "No relevant information found.", "urls": "No relevant information found."}
            full_text = "\n\n".join(c['content'] for c in contexts if 'content' in c)
            urls = "\n\n".join(c.get('url', 'No URL provided') for c in contexts)
            return {"full_text": full_text, "urls": urls}
        except Exception as e:
            error_msg = f"Error during search: {e}"
            return {"full_text": error_msg, "urls": error_msg}

    def process_query(self, query):
        clean_query = query[1:].strip() if query.startswith('/') else query
        print(f"Using search query: '{clean_query}'")
        search_result = self.get_search_context(clean_query)
        print("\nURLs obtained from search:")
        print(search_result["urls"])
        try:
            doc_name = f"Supporting info for query: {clean_query}"
            # Store the full text (not just the URLs) in the FAISS index
            importdocs.update_collection_with_text(doc_name, search_result["full_text"])
            print("Supporting info stored in RAG.")
        except Exception as e:
            print(f"Error storing supporting info in RAG: {e}")
        return search_result

if __name__ == "__main__":
    cloud_service_url = "https://edneorfuvixmugzdyuhr.supabase.co/functions/v1/ratelimit"
    ollama_url = "http://localhost:11434"
    current_model = "example-model"  # Replace with your actual model name.
    api_key = "YOUR_API_KEY"  # Replace with your API key for testing.
    searcher = SimpleSearch(cloud_service_url, ollama_url, current_model, api_key)
    test_query = "/What is the impact of climate change on polar bears?"
    context = searcher.process_query(test_query)
    print("\nReturned search result:")
    print(context)
