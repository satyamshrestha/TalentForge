from repositories.user_repository import UserRepository
from services.user_service import UserService

def get_user_service():
    repository = UserRepository()
    return UserService(repository)