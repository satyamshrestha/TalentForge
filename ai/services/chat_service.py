from ai.provider_factory import get_provider


class ChatService:
    def __init__(self):
        self.provider = get_provider()

    def chat(self, prompt: str) -> str:
        return self.provider.generate(prompt)