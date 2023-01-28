from dataclasses import dataclass, field
from datetime import timedelta
from typing import List


@dataclass
class TestResult:
    test_id: int = None
    success: bool = True
    std_err: str = ""
    time_duration_in_seconds: timedelta = timedelta(seconds=0)

    def to_dict(self) -> dict:
        return {
            "test_id": self.test_id,
            "success": self.success,
            "std_err": self.std_err,
            "time_duration_in_seconds": self.time_duration_in_seconds.total_seconds()
        }


@dataclass
class TaskResults:
    task_id: int = None
    test_results: List[TestResult] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "test_results": [test_result.to_dict() for test_result in self.test_results]
        }
