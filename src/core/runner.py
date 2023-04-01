import datetime
import io
import shutil
from subprocess import run, PIPE, Popen

from models import TestResult


class AlgorithmTestRunner:
    def __init__(self, test_cases: dict[str, list] = None):
        """
        Вспомогательные ссылки
        https://docs.python.org/3/library/subprocess.html
        :param subprocess:
        """
        self.test_cases = test_cases

    def run_tests(self):

        results = []

        for to_stdin in self.test_cases.keys():
            with Popen(["python3", "-m", "students_solution.py"], stderr=PIPE, stdout=PIPE, stdin=PIPE,
                       universal_newlines=True,
                       bufsize=len(self.test_cases.keys())) as process:
                time_start = datetime.datetime.now()

                result_out, error = process.communicate(to_stdin)
                time_end = datetime.datetime.now()
                print(result_out.strip().split("\n"))
                print(error)

                test_result = TestResult()
                test_result.time_duration_in_seconds = (time_end - time_start).total_seconds()
                if error:
                    test_result.success = False
                    test_result.std_err = error
                else:
                    test_result.success = True

                results.append(test_result)

        print(results)
