from pypdf import PdfReader

from ai.services.resume_analyzer import ResumeAnalyzer
from db.database import SessionLocal
from db.redis import redis_client
from models.resume import Resume
from services.resume_parser import ResumeParser
from tasks.celery_app import celery
from exceptions.ai_exception import AIProviderException


@celery.task(
    bind=True,
    max_retries=3
)
def process_resume(self, id: str):
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

        cache_key = f"user:{resume.user_id}:resumes"

        resume.status = "PROCESSING"
        resume.error_message = None
        db.commit()

        redis_client.delete(cache_key)

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

        redis_client.delete(cache_key)

    except AIProviderException as e:
        db.rollback()

        if self.request.retries >= self.max_retries:
            if resume:
                resume.status = "FAILED"
                resume.error_message = str(e)
                db.commit()

                cache_key = f"user:{resume.user_id}:resumes"
                redis_client.delete(cache_key)

            raise

        raise self.retry(
            exc=e,
            countdown=10
        )

    except Exception as e:
        db.rollback()

        if resume:
            resume.status = "FAILED"
            resume.error_message = str(e)
            db.commit()

            cache_key = f"user:{resume.user_id}:resumes"
            redis_client.delete(cache_key)

        raise

    finally:
        db.close()