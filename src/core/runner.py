import io
import shutil
from subprocess import run, PIPE, Popen


class AlgorithmTestRunner:
    def __init__(self, test_cases: dict[str, list] = None, file_to_run: io.StringIO = None):
        """
        Вспомогательные ссылки
        https://docs.python.org/3/library/subprocess.html
        :param subprocess:
        """
        self.test_cases = test_cases
        self.students_code = file_to_run

    def _create_solution_python_file(self):
        with open("students_solution.py", "w") as solution_writer:
            self.students_code.seek(0)
            shutil.copyfileobj(self.students_code, solution_writer)

    def run_tests(self):
        self._create_solution_python_file()

        results = []

        with Popen(["python3", "students_solution.py"], stderr=PIPE, stdout=PIPE, stdin=PIPE, universal_newlines=True,
                   bufsize=1) as process:
            for to_stdin in self.test_cases.keys():
                print(to_stdin)
                process.stdin.write(to_stdin + "\n")

                data = process.stdout.read().strip().split("\n")
                print(data)
                results.append(
                    "+" if data == self.test_cases.get(to_stdin) else "-"
                )

        print(results)
