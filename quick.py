from ai.services.chat_service import ChatService

service = ChatService()

print(
    service.chat(
        "Explain FastAPI in one paragraph."
    )
)