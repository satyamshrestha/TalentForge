import logging
import requests

from ai.providers.base import LLMProvider
from exceptions.ai_exception import AIProviderException
from utils.config import settings


logger = logging.getLogger("talentforge")


class OllamaProvider(LLMProvider):
    """LLM provider implementation using Ollama."""

    def generate(self, prompt: str) -> str:
        for attempt in range(settings.OLLAMA_RETRIES):

            try:
                response = requests.post(
                    f"{settings.OLLAMA_BASE_URL}/api/generate",
                    json={
                        "model": settings.LLM_MODEL,
                        "prompt": prompt,
                        "stream": False,
                        "format": "json"
                    },
                    timeout=settings.OLLAMA_TIMEOUT,
                )
                response.raise_for_status()
                data = response.json()
                return data["response"]

            except requests.RequestException as e:
                logger.warning(
                    "Ollama request failed. Attempt %s/%s. Error=%s",
                    attempt + 1,
                    settings.OLLAMA_RETRIES,
                    str(e)
                )

                if attempt == settings.OLLAMA_RETRIES - 1:
                    logger.error(
                        "Ollama provider unavailable after %s attempts.",
                        settings.OLLAMA_RETRIES
                    )
                    raise AIProviderException()