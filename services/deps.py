from repositories.answer_repository import AnswerRepository
from repositories.audit_log_repository import AuditLogRepository
from repositories.dashboard_repository import DashboardRepository
from repositories.interview_repository import InterviewRepository
from repositories.question_repository import QuestionRepository
from repositories.resume_repository import ResumeRepository
from repositories.user_repository import UserRepository
from services.answer_evaluator import AnswerEvaluator
from services.answer_service import AnswerService
from services.audit_log_service import AuditLogService
from services.dashboard_service import DashboardService
from services.interview_service import InterviewService
from services.question_generator import QuestionGenerator
from services.resume_service import ResumeService
from services.user_service import UserService

def get_audit_log_service():
    return AuditLogService(
        AuditLogRepository()
    )

def get_user_service():
    return UserService(UserRepository())

def get_resume_service():
    return ResumeService(ResumeRepository())

def get_interview_service():
    return InterviewService(
        InterviewRepository(),
        QuestionRepository(),
        ResumeRepository(),
        QuestionGenerator(),
        get_audit_log_service()
    )

def get_answer_service():
    return AnswerService(
        AnswerRepository(),
        AnswerEvaluator(),
        QuestionRepository(),
        InterviewRepository(),
        get_audit_log_service()
    )

def get_dashboard_service():
    return DashboardService(
        DashboardRepository()
    )