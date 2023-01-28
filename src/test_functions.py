import io
from pathlib import Path

from core.runner import AlgorithmTestRunner

if __name__ == '__main__':
    py_solution = io.StringIO(Path("tmp_1.py").read_text())

    test_runner = AlgorithmTestRunner(
        test_cases={
            "1 3": ["-2", "4"],
            "3 1": ["2", "4"]
        },
        file_to_run=py_solution
    )

    test_runner.run_tests()
