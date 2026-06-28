from sqlalchemy.orm import Session

from models.user import User
from repositories.dashboard_repository import DashboardRepository
from repositories.interview_repository import InterviewRepository

class DashboardService:

    def __init__(
        self,
        dashboard_repository: DashboardRepository,
        interview_repository: InterviewRepository
    ):
        self.dashboard_repository = dashboard_repository
        self.interview_repository = interview_repository
    
    def get_dashboard(
        self,
        db: Session,
        current_user: User
    ):
        total_resumes = self.dashboard_repository.get_total_resumes(db, current_user.id)
        total_interviews = self.dashboard_repository.get_total_interviews(db, current_user.id)
        completed_interviews = self.dashboard_repository.get_completed_interviews(db, current_user.id)
        interviews = self.interview_repository.get_interviews(db, current_user.id)
        total_score = 0
        total_answers = 0
        for interview in interviews:
            for question in interview.questions:
                if question.answer:
                    total_answers += 1
                    total_score += int(question.answer.score)
        average_interview_score = (
            total_score/total_answers
            if total_answers
            else 0
        )
        recent_interviews = self.dashboard_repository.get_recent_interviews(db, current_user.id)
        return {
            "total_resumes": total_resumes,
            "total_interviews": total_interviews,
            "completed_interviews": completed_interviews,
            "average_interview_score": round(average_interview_score, 2),
            "recent_interviews": recent_interviews
        }