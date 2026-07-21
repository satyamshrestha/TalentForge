from tasks.celery_app import celery
from pypdf import PdfReader

from db.database import SessionLocal
from models.resume import Resume
from services.resume_parser import ResumeParser
from ai.services.resume_analyzer import ResumeAnalyzer

@celery.task
def process_resume(id: str):
    db = SessionLocal()
    parser = ResumeParser()
    analyzer = ResumeAnalyzer()
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

        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )
            
        parsed_data = parser.parse(text)
        analysis = analyzer.analyze(text)

        parsed_data["pages"] = len(reader.pages)
        parsed_data["ai_analysis"] = analysis.model_dump()

        resume.parsed_text = parsed_data
        resume.status = "COMPLETED"
        resume.error_message = None

        db.commit()

    except Exception as e:
        if resume:
            resume.status = "FAILED"
            resume.error_message = repr(e)
            db.commit()

    finally:
        db.close()