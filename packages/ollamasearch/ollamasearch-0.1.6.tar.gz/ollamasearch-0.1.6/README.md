# OllamaSearch

A Python package for intregating ollama with web with Web Serach and RAG.

## Installation

pip install ollamasearch


## Configuration

The application uses a `.env` file in the project root to store the API key for the external search service. If the file doesn't exist, the application will create it and prompt you for the key on the first run.

```
# .env
API_KEY=your_search_service_api_key
```

## Usage

Once installed, you can run the interactive chat application using the command line:

```bash
ollamasearch
```

The application will:
1.  Ask you to enter your search service API key if not found in `.env`.
2.  Fetch available Ollama models running locally (ensure Ollama is running at `http://localhost:11434`).
3.  Prompt you to select a model.
4.  Start the chat interface.

**Chat Commands:**
*   Type your query directly to perform a RAG search using the local FAISS index.
*   Prefix your query with `/` (e.g., `/what is ollama?`) to perform a web search.
*   Type `//api_key` to update the search service API key stored in `.env`.
*   Type `//exit` to quit the application.

## Functionality

*   **Chat Interface:** Interactive command-line chat.
*   **Model Selection:** Choose from locally available Ollama models.
*   **RAG Search:** Uses a FAISS index built from provided documents or web search results to augment prompts sent to Ollama.
*   **Web Search Integration:** Queries starting with `/` trigger an external web search to gather context.
