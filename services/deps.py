from repositories.user_repository import UserRepository
from repositories.resume_repository import ResumeRepository
from services.user_service import UserService
from services.resume_service import ResumeService

def get_user_service():
    repository = UserRepository()
    return UserService(repository)

def get_resume_service():
    repository = ResumeRepository()
    return ResumeService(repository)