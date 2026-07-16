import requests

from ai.providers.base import LLMProvider
from utils.config import settings


class OllamaProvider(LLMProvider):
    """LLM provider implementation using Ollama."""
    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": settings.LLM_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=settings.OLLAMA_TIMEOUT,
        )

        response.raise_for_status()

        data = response.json()
        return data["response"]