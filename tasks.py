from celery_app import celery
from pypdf import PdfReader

from db.database import SessionLocal
from models.resume import Resume


@celery.task
def process_resume(id: str):
    db = SessionLocal()
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

        pages = []
        full_text = ""

        for page in reader.pages:

            page_text = page.extract_text() or ""

            pages.append(page_text)

            full_text += page_text + "\n"

        resume.parsed_text = {
            "raw_text": full_text.strip(),
            "pages": len(reader.pages)
        }

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