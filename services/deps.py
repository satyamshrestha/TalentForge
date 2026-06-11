from repositories.user_repository import UserRepository
from repositories.resume_repository import ResumeRepository
from repositories.interview_repository import InterviewRepository
from services.user_service import UserService
from services.resume_service import ResumeService
from services.question_generator import QuestionGenerator
from services.interview_service import InterviewService

def get_user_service():
    repository = UserRepository()
    return UserService(repository)

def get_resume_service():
    repository = ResumeRepository()
    return ResumeService(repository)

def get_interview_service():
    return InterviewService(
        InterviewRepository(),
        ResumeRepository(),
        QuestionGenerator()
    )