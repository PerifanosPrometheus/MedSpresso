"""Ollama API client for MedSpresso."""
import requests
from typing import Iterator, Optional
from pathlib import Path
import json

OLLAMA_API_URL = "http://localhost:11434/api"

class OllamaClient:
    def __init__(self, model: str):
        self.model = model
        self.base_url = OLLAMA_API_URL
    
    def generate(self, prompt: str, stream: bool = True) -> Iterator[str]:
        """Generate text from the model."""
        response = requests.post(
            f"{self.base_url}/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": stream
            },
            stream=stream
        )
        response.raise_for_status()
        
        if stream:
            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line)
                    if 'response' in json_response:
                        yield json_response['response']
        else:
            json_response = response.json()
            yield json_response['response']
    
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