from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass