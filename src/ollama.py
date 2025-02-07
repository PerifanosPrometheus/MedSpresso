"""Ollama API client for MedSpresso."""
import requests
from typing import Optional
from rich.console import Console

console = Console()
OLLAMA_API_URL = "http://localhost:11434/api"

class OllamaClient:
    def __init__(self, model: str, system: Optional[str] = None):
        self.model = model
        self.system = system
        self.base_url = OLLAMA_API_URL
        
        # Check if Ollama is running
        try:
            requests.get(f"{self.base_url}/tags")
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "Cannot connect to Ollama. Please make sure Ollama is installed and running:\n"
                "1. Install: brew install ollama\n"
                "2. Start: ollama serve\n"
                "3. Pull model: ollama pull " + model
            )
    
    def generate(self, prompt: str) -> str:
        """Generate text from the model."""
        try:
            response = requests.post(
                f"{self.base_url}/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "system": self.system,
                    "stream": False
                }
            )
            response.raise_for_status()
            
            json_response = response.json()
            if 'error' in json_response:
                raise Exception(f"Ollama error: {json_response['error']}")
            
            return json_response['response']
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"HTTP error occurred: {e}")
        except Exception as e:
            raise Exception(f"Error during generation: {e}")
    
    @classmethod
    def list_models(cls) -> list[str]:
        """List available local models."""
        response = requests.get(f"{OLLAMA_API_URL}/tags")
        response.raise_for_status()
        return [model['name'] for model in response.json()['models']]
    
    @classmethod
    def pull_model(cls, model: str) -> None:
        """Pull a model from Ollama."""
        response = requests.post(
            f"{OLLAMA_API_URL}/pull",
            json={"name": model},
            stream=True
        )
        response.raise_for_status() 