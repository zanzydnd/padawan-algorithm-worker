import datetime
import logging
from subprocess import Popen
from typing import List
from subprocess import PIPE, Popen

logger = logging.getLogger()


class ScenarioRunner:
    def __init__(self, scenario_dict: dict, ident: str):
        self.return_data = {}
        self.data_container = {}
        self.scenario_dict = scenario_dict
        self.ident = ident

    def run(self):
        for scenario_step in self.scenario_dict.get("steps"):
            with Popen(["python3", "-m", self.ident], stderr=PIPE, stdout=PIPE, stdin=PIPE,
                       universal_newlines=True,
                       bufsize=len(scenario_step.get("input"))) as process:
                time_start = datetime.datetime.now()

                result_out, error = process.communicate(scenario_step.get("input"))
                time_end = datetime.datetime.now()

                self.return_data[scenario_step.get("id")] = {
                    "time": {
                        "success": (time_end - time_start).seconds < scenario_step.get("time"),
                        "actual": (time_end - time_start).seconds
                    },
                    "comparison": {
                        "success": result_out.strip("\n") == scenario_step.get("expected"),
                        "actual": result_out.strip("\n")
                    }
                }


class TestRunner:
    def __init__(self, submission_id: int, scenarios: List[dict], ident: str):
        self.submission_id = submission_id
        self.scenarios = scenarios
        self.ident = ident
        self.scenario_runners = []
        self.result_data = []
        self.data = []

    def run(self):
        logger.info("Test running")
        for scenario_dict in self.scenarios:
            scenario_runner = ScenarioRunner(
                scenario_dict=scenario_dict,
                ident=self.ident
            )
            self.scenario_runners.append(scenario_runner)
            scenario_runner.run()

    def create_result_data(self, submission_id):
        return {
            "submission_id": submission_id,
            "scenarios": {
                scenario_runner.scenario_dict.get("id"): scenario_runner.return_data
                for scenario_runner in self.scenario_runners
            }
        }
