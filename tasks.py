from celery_app import celery
from pypdf import PdfReader

from db.database import SessionLocal
from models.resume import Resume
from services.resume_parser import ResumeParser

@celery.task
def process_resume(id: str):
    db = SessionLocal()
    parser = ResumeParser()
    resume = None

    try:
        resume = (
            db.query(Resume)
            .filter(Resume.id == id)
            .first()
        )

        if not resume:
            return

        resume.status = "PROCESSING"
        resume.error_message = None
        db.commit()

        reader = PdfReader(resume.file_path)

        text = ""

        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
            
        parsed_data = parser.parse(text)
        parsed_data["pages"] = len(reader.pages)
        resume.parsed_text = parsed_data

        resume.status = "COMPLETED"
        resume.error_message = None

        db.commit()

    except Exception as e:
        if resume:
            resume.status = "FAILED"
            resume.error_message = str(e)
            db.commit()

    finally:
        db.close()