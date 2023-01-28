from .celery_main import celery_app


@celery_app.task(name='remote.check_student_solution')
def check_student_solution():
    pass
