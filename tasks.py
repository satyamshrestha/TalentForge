from celery_app import celery

@celery.task
def add(a, b):
    return a+b