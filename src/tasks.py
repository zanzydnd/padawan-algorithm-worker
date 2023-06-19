from typing import List
from uuid import uuid4

import requests

from src.accessors.git_accessor import GitAccessor
from src.testing import TestRunner
from src.celery_main import celery_app


def prepare(git_url: str, ident: str):
    git_accessor = GitAccessor()
    git_accessor.pull_repository(git_url, ident)

    return git_accessor


def clean_up(ident: str, git_accessor: GitAccessor):
    git_accessor.delete_local_repository(ident)


@celery_app.task(name='remote.test_alg_submission')
def check_student_solution(
        submission_id: int, scenarios: List[dict], git_url: str
):

    ident = str(uuid4())[:8]

    git_accessor = prepare(git_url, ident)

    test_runner = TestRunner(submission_id, scenarios, ident)
    test_runner.run()

    clean_up(ident, git_accessor)
    requests.post("http://127.0.0.1:8000/api/v1/submission_result/", json=test_runner.create_result_data(submission_id))
