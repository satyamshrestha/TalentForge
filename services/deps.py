from repositories.answer_repository import AnswerRepository
from repositories.interview_repository import InterviewRepository
from repositories.question_repository import QuestionRepository
from repositories.resume_repository import ResumeRepository
from repositories.user_repository import UserRepository
from services.answer_evaluator import AnswerEvaluator
from services.answer_service import AnswerService
from services.interview_service import InterviewService
from services.question_generator import QuestionGenerator
from services.resume_service import ResumeService
from services.user_service import UserService

def get_user_service():
    repository = UserRepository()
    return UserService(repository)

def get_resume_service():
    repository = ResumeRepository()
    return ResumeService(repository)

def get_interview_service():
    return InterviewService(
        InterviewRepository(),
        QuestionRepository(),
        ResumeRepository(),
        QuestionGenerator()
    )

def get_answer_service():
    return AnswerService(
        AnswerRepository(),
        AnswerEvaluator(),
        QuestionRepository()
    )