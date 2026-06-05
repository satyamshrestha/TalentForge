from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.deps import get_current_user
from db.deps import get_db
from models.user import User
from schemas.resume_schema import ResumeCreate, ResumeResponse, ResumeUpdate
from services.deps import get_resume_service
from services.resume_service import ResumeService

router = APIRouter(prefix="/resumes", tags=["Resume"])

@router.post("/", response_model=ResumeResponse)
def create_resume(
    data: ResumeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: ResumeService = Depends(get_resume_service)
):
    return service.create_resume(
        db,
        current_user,
        data.file_url,
        data.parsed_text
    )

@router.get("/me", response_model=list[ResumeResponse])
def get_my_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: ResumeService = Depends(get_resume_service)
):
    return service.get_my_resumes(db, current_user)

@router.get("/{id}", response_model=ResumeResponse)
def get_resume_by_id(
    id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: ResumeService = Depends(get_resume_service)
):
    return service.get_resume(db, id, current_user)

@router.put("/{id}", response_model=ResumeResponse)
def update_resume(
    id: str,
    data: ResumeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: ResumeService = Depends(get_resume_service)
):
    return service.update_resume(
        db, 
        id=id,
        current_user=current_user,
        file_url=data.file_url,
        parsed_text=data.parsed_text
    )

@router.delete("/{id}")
def delete_resume(
    id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: ResumeService = Depends(get_resume_service)
):
    service.delete_resume(db, id, current_user)
    return {
        "message": "Resume Deleted Successfully!"
    }