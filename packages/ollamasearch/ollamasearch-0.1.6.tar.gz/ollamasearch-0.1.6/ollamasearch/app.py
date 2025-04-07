# app.py
import requests
import json
import pathlib  # Use pathlib for path manipulation
from platformdirs import user_config_dir # For cross-platform config directory
from .simplesearch import SimpleSearch
from .search import perform_search
from . import importdocs
# Removed check import and call

# Define the application name and author for platformdirs
APP_NAME = "ollamasearch"
APP_AUTHOR = "Nikhil" # Or a more generic author if preferred

class ChatWrapper:
    def __init__(self):
        self.cloud_service_url = "http://localhost:8000"
        self.ollama_url = "http://localhost:11434/api/chat"
        self.api_key = None
        self.available_models = []
        self.current_model = None
        self.simple_search = None
        self.history = []
        self._config_path = self._get_config_path()
        self._load_config() # Load config on initialization

    def get_available_models(self):
        """Fetch available models from Ollama."""
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.get("http://localhost:11434/api/tags", headers=headers)
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        except Exception as e:
            print(f"Error getting models: {e}")
            return []

    def select_model(self):
        """Allow the user to select a model from the available ones."""
        self.available_models = self.get_available_models()
        if not self.available_models:
            print("No models available. Please install or configure models first.")
            return False

        print("\nAvailable models:")
        for i, model in enumerate(self.available_models, 1):
            print(f"{i}. {model}")

        while True:
            try:
                choice = int(input("\nSelect model (number): "))
                if 1 <= choice <= len(self.available_models):
                    self.current_model = self.available_models[choice - 1]
                    print(f"Selected model: {self.current_model}")
                    # Ensure API key is loaded before creating SimpleSearch
                    if self.api_key:
                        self.simple_search = SimpleSearch(
                            self.cloud_service_url,
                            self.ollama_url,
                            self.current_model,
                            self.api_key
                        )
                    else:
                        # This case should ideally be handled before model selection
                        # but adding a safeguard here.
                        print("Error: API key not set. Cannot initialize search.")
                        return False
                    return True
                print("Invalid selection. Try again.")
            except ValueError:
                print("Please enter a valid number.")

    def _get_config_path(self):
        """Get the path to the configuration file."""
        config_dir = pathlib.Path(user_config_dir(APP_NAME, APP_AUTHOR))
        return config_dir / "config.json"

    def _load_config(self):
        """Load configuration from the JSON file."""
        try:
            self._config_path.parent.mkdir(parents=True, exist_ok=True) # Ensure dir exists
            if self._config_path.exists():
                with open(self._config_path, "r") as f:
                    config_data = json.load(f)
                    self.api_key = config_data.get("API_KEY")
        except (FileNotFoundError, json.JSONDecodeError, OSError) as e:
            print(f"Could not load config file: {e}. Will prompt for API key if needed.")
            self.api_key = None # Ensure key is None if loading fails

    def _save_config(self):
        """Save the current configuration (API key) to the JSON file."""
        try:
            self._config_path.parent.mkdir(parents=True, exist_ok=True) # Ensure dir exists
            config_data = {"API_KEY": self.api_key}
            with open(self._config_path, "w") as f:
                json.dump(config_data, f, indent=4)
        except OSError as e:
            print(f"Error saving config file: {e}")

    def call_ollama(self, query):
        """Send a query to Ollama and stream the response."""
        self.history.append({"role": "user", "content": query})
        payload = {
            "model": self.current_model,
            "messages": self.history,
            "stream": True
        }
        headers = {"Content-Type": "application/json"}
        try:
            with requests.post(self.ollama_url, json=payload, headers=headers, stream=True) as response:
                response.raise_for_status()
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        content = chunk.get("message", {}).get("content", "")
                        print(content, end="", flush=True)
                        full_response += content
                print()  # Newline after streaming
                self.history.append({"role": "assistant", "content": full_response})
        except Exception as e:
            print(f"Error calling Ollama: {e}")

    def process_query(self, query):
        """Process the user query using the appropriate pipeline."""
        perform_search(query, self.current_model, self.api_key)

    def handle_api_key_change(self):
        """Allow the user to change the API key."""
        new_key = input("Enter new API key: ").strip()
        if not new_key:
            print("No key provided. Operation canceled.")
            return

        # Update current instance and save to config file
        self.api_key = new_key
        self._save_config() # Save the updated key

        if self.current_model:
            self.simple_search = SimpleSearch(
                self.cloud_service_url,
                self.ollama_url,
                self.current_model,
                self.api_key
            )
        print("API key updated successfully.")

    def start_chat(self):
        """Start the chat session."""
        # API key is loaded in __init__ via _load_config()
        if not self.api_key:
            print("API key not found in configuration.")
            self.api_key = input("Enter your API key: ").strip()
            if not self.api_key:
                print("API key is required. Exiting...")
                return
            # Save the newly entered key
            self._save_config()

        # Now that the key is guaranteed (either loaded or entered), select model
        if not self.select_model():
            # If model selection fails (e.g., no models), exit
            return

        print("\nChat started. Type '//exit' to quit. Type '//api_key' to change API key.")
        while True:
            try:
                query = input("\n>>> ").strip()
                if query == "//exit":
                    print("Exiting...")
                    break
                if query == "//api_key":
                    self.handle_api_key_change()
                    continue
                if not query:
                    continue

                print("\nProcessing...")
                self.process_query(query)

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"\nError: {e}")

def main():
    wrapper = ChatWrapper()
    wrapper.start_chat()

if __name__ == "__main__":
    main()
