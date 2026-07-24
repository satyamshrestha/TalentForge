from ai.providers.openai_provider import OpenAIProvider
from ai.providers.ollama_provider import OllamaProvider
from ai.providers.base import LLMProvider
from utils.config import settings

def get_provider() -> LLMProvider:
    if settings.LLM_PROVIDER == "openai":
        return OpenAIProvider()

    if settings.LLM_PROVIDER == "ollama":
        return OllamaProvider()

    raise ValueError(
        f"Unsupported LLM provider: {settings.LLM_PROVIDER}"
    )