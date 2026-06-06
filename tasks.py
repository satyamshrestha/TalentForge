from celery_app import celery

@celery.task
def process_resume(id: str):
    print(f"Processing resume {id}.")