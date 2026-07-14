from ai.providers.base import LLMProvider

class OllamaProvider(LLMProvider):

    def generate(self, prompt: str) -> str:
        raise NotImplementedError