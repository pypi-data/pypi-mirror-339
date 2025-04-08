"""
TestStatus module
"""

import json
from abc import ABC, abstractmethod
from typing import Dict, List
from functools import cmp_to_key
from robot.libraries.BuiltIn import BuiltIn, keyword
from skyramp.test_status import _get_response_value, ResponseLog, TesterState
from skyramp.test_status import TestResultType, TestStat, RawTestResult
from skyramp.utils import sanitize_payload, sanitize_headers_and_cookies


class AsyncTestStatus(ABC):
    """
    AsyncTestStatus object
    """

    test_id: str = ""
    test_type: str = ""

    def __init__(self, options: dict):
        self.options = options

    def get_test_id(self):
        """
        Returns the test id
        """
        return self.test_id

    def get_test_type(self):
        """
        Returns the test type
        """
        return self.test_type

    @abstractmethod
    def get_scenario(self, scenario_name) -> "BaseAsyncScenarioStatus":
        """
        Get the scenario
        """

    @abstractmethod
    def get_scenarios(self, scenario_name: str = "") -> List["BaseAsyncScenarioStatus"]:
        """
        Get the scenarios
        """

    @abstractmethod
    def get_request(
        self, scenario_name: str, request_name: str
    ) -> "BaseAsyncRequestStatus":
        """
        Get the request
        """

    @abstractmethod
    def get_overall_status(self) -> Dict[str, str]:
        """
        Get the overall status
        """

    @staticmethod
    def create(options: dict):
        """
        Create the appropriate TestStatus object based on the options
        """
        if (
            "results" in options
            and len(options["results"]) > 1
            and "type" in options["results"][1]
            and options["results"][1]["type"] == "load"
        ):
            return AsyncLoadTestStatus(options)
        return AsyncIntegrationTestStatus(options)


class BaseAsyncRequestStatus(ABC):
    """
    BaseAsyncRequestStatus object
    """

    def __init__(self, result_object: dict):
        self.name = ""
        self.id = ""
        self.result_object = ""
        self.json_object = result_object

    def __repr__(self):
        return f"BaseAsyncRequestStatus(name={self.name}, status={self.result_object})"

    @abstractmethod
    def get_load_test_response(self, status_code: str, json_path: str = None) -> str:
        """
        Get the response of the load test
        """

    @abstractmethod
    def get_response(self, json_path: str = None) -> str:
        """
        Get the response of the request
        """

    @abstractmethod
    def get_var_value(self, key: str) -> str:
        """
        Get the value of the variable
        """


class BaseAsyncScenarioStatus(ABC):
    """
    BaseAsyncScenarioStatus object
    """

    def __init__(self, data_object: dict):
        self.result: str = data_object
        self.name = ""
        self.overall_status = {}
        self.timeseries = []
        self.sub_scenarios: List["BaseAsyncScenarioStatus"] = []
        self.requests: List["BaseAsyncRequestStatus"] = []

    @abstractmethod
    def get_sub_scenarios(self) -> List["BaseAsyncScenarioStatus"]:
        """
        Get the sub scenarios
        """

    @abstractmethod
    def get_request(self, request_name: str) -> "BaseAsyncRequestStatus":
        """
        Get the request based on the request name
        """

    @abstractmethod
    def get_requests(self) -> List["BaseAsyncRequestStatus"]:
        """
        Get the requests
        """

    @abstractmethod
    def get_overall_status(self) -> Dict[str, str]:
        """
        Get the overall status
        """


class AsyncLoadTestStatus(AsyncTestStatus):
    """
    AsyncTestTypeStatus object
    """

    class AsyncScenarioStatus(BaseAsyncScenarioStatus):
        """
        AsyncScenarioStatus object
        """

        def __init__(self, data_object: dict):
            super().__init__({})
            data_object = TestStat(data_object)
            self.result: str = data_object
            self.name = data_object.description.split(".")[-1]
            self.id = data_object.id
            self.overall_status: TestStat = data_object
            self.sub_scenarios: List["AsyncLoadTestStatus.AsyncScenarioStatus"] = []
            self.requests: List["AsyncLoadTestStatus.AsyncRequestStatus"] = []

        # pylint: disable=line-too-long
        def __repr__(self):
            return f"AsyncScenarioStatus(name={self.name}, status={self.overall_status.__repr__()}, sub_scenarios={self.sub_scenarios}, requests={self.requests})"

        def __str__(self):
            # iterate over the requests and get the request status
            request_status = []
            for request in self.requests:
                # iterate over the request table and get the request status
                log_tables = request.result_object.log_table
                for status_code, json_data in log_tables.items():
                    log_tables[status_code] = json.loads(json_data)
                request_status.append(request.to_json())
            return json.dumps(
                {
                    "name": self.name,
                    "status": self.overall_status.to_json(),
                    # "sub_scenarios": self.sub_scenarios,
                    "requests": request_status,
                },
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
            )

        def get_sub_scenarios(self) -> List["AsyncLoadTestStatus.AsyncScenarioStatus"]:
            # sort the sub scenarios based on the id
            self.sub_scenarios.sort(key=cmp_to_key(_sort_keys))
            return self.sub_scenarios

        def get_request(
            self, request_name: str
        ) -> "AsyncLoadTestStatus.AsyncRequestStatus":
            request_list = []
            for request in self.requests:
                if request.result_object.description.endswith("." + request_name):
                    request_list.append(request)
            if len(request_list) == 1:
                return request_list[0]
            # throw error that request not found
            if len(request_list) == 0:
                raise KeyError(f"Request {request_name} not found in the scenario")
            # throw error that multiple requests found
            if len(request_list) > 1:
                raise KeyError(
                    f"Multiple requests found with the name {request_name},please iterate over the requests"
                )
            return None

        def get_requests(self) -> List["AsyncLoadTestStatus.AsyncRequestStatus"]:
            self.requests.sort(key=cmp_to_key(_sort_keys))
            return self.requests

        def get_overall_status(self) -> Dict[str, str]:
            return self.overall_status

    class AsyncRequestStatus(BaseAsyncRequestStatus):
        """
        AsyncRequestStatus object
        """

        def __init__(self, result_object: dict):
            super().__init__(result_object)
            result_object = TestStat(result_object)
            self.name = result_object.description.split(".")[-1]
            self.id = result_object.id
            self.result_object = result_object

        def __repr__(self):
            return f"AsyncRequestStatus(name={self.name}, status={self.result_object})"

        def to_json(self):
            """
            Convert the object to json
            """
            return {
                "name": self.name,
                "status": self.result_object.to_json(),
            }

        def get_load_test_response(
            self, status_code: str, json_path: str = None
        ) -> str:
            json_data = self.result_object.log_table.get(status_code, None)
            if json_data is None:
                return None
            json_response = json.loads(json_data).get("Response", None)
            if json_response is not None:
                payload = json_response.get("payload", None)
                if json_response is None:
                    return None
                if json_path is None:
                    return json.dumps(payload, indent=2)
                return _get_response_value(payload, json_path)
            return None

        def get_response(self, json_path: str = None) -> str:
            raise NotImplementedError

        def get_var_value(self, key: str) -> str:
            raise NotImplementedError

    scenario_dict: Dict[str, AsyncScenarioStatus] = {}

    def __init__(self, options: dict):
        super().__init__(options)
        self.test_id = options.get("id", "")
        self.test_type = "load"
        if options and options.get("results") is None:
            return
        results = options["results"]
        for result in results[1:]:
            raw_result = RawTestResult(result)
            stats = raw_result.stat
            for key, result in stats.items():
                result_stat = TestStat(result)
                result["id"] = key
                result_id = result_stat.description
                if result_stat.type == TestResultType.Scenario:
                    new_scenario = AsyncLoadTestStatus.AsyncScenarioStatus(result)
                    # if id does not have . then it is a top level scenario
                    if "." not in result_id:
                        new_scenario.timeseries = raw_result.timeseries
                    self.scenario_dict[result_id] = new_scenario
                elif result_stat.type == TestResultType.Request:
                    # keep dropping the .<> from the result_id to get the parent scenario
                    item_list = result_id.split(".")
                    for i in reversed(range(len(item_list))):
                        item_list.pop(i)
                        parent_scenario = ".".join(item_list[:-1])
                        if parent_scenario in self.scenario_dict:
                            request = AsyncLoadTestStatus.AsyncRequestStatus(result)
                            self.scenario_dict[parent_scenario].requests.append(request)
                            break

    def get_scenario(self, scenario_name) -> AsyncScenarioStatus:
        scenario_list = self.get_scenarios(scenario_name)
        if len(scenario_list) == 1:
            return scenario_list[0]
        # throw error that scenario not found
        if len(scenario_list) == 0:
            raise KeyError(f"Scenario {scenario_name} not found in the test")
        # throw error that multiple scenarios found
        if len(scenario_list) > 1:
            # pylint: disable=line-too-long
            raise KeyError(
                f"Multiple scenarios found with the name {scenario_name},please iterate over the scenarios"
            )
        return None

    def get_scenarios(self, scenario_name: str = "") -> List[AsyncScenarioStatus]:
        # sort the scenarios based on the id
        scenario_list = sorted(self.scenario_dict.values(), key=cmp_to_key(_sort_keys))
        if scenario_name == "":
            return list(scenario_list)
        scenarios = []
        # iterate over the scenario_dict and get scenario for the given scenario_name
        for scenario in scenario_list:
            if scenario.name == scenario_name:
                scenarios.append(scenario)
        return scenarios

    def get_request(self, scenario_name: str, request_name: str) -> AsyncRequestStatus:
        scenario = self.get_scenario(scenario_name)
        return scenario.get_request(request_name)

    def get_overall_status(self) -> Dict[str, str]:
        overall_status = []
        # iterate through top level scenarios and get the overall status
        for scenario_name, scenario in self.scenario_dict.items():
            if len(scenario_name.split(".")) == 2:
                scenario_status = scenario.get_overall_status()
                scenario_status.name = scenario.name
                overall_status.append(scenario.get_overall_status())
        return overall_status


class AsyncIntegrationTestStatus(AsyncTestStatus):
    """
    AsyncIntegrationTestStatus object
    """

    class AsyncScenarioStatus(BaseAsyncScenarioStatus):
        """
        AsyncScenarioStatus object
        """

        def __init__(self, data: dict):
            super().__init__(data)
            data = RawTestResult(data)
            desc_list = data.description.split(".")
            self.name: str = desc_list[-1]
            self.id = data.id
            self.status = data.status
            self.error = data.error
            self.step_description = data.step_description
            self.step_name = data.step_name
            self.sub_scenarios: List[
                "AsyncIntegrationTestStatus.AsyncScenarioStatus"
            ] = []
            self.requests: List["AsyncIntegrationTestStatus.AsyncRequestStatus"] = []

        # pylint: disable=line-too-long
        def __repr__(self):
            return f"AsyncScenarioStatus(name={self.name}, status={self.status.__repr__()}, error={self.error})"

        def get_sub_scenarios(
            self,
        ) -> List["AsyncIntegrationTestStatus.AsyncScenarioStatus"]:
            """
            Get sub scenarios from the scenario
            """
            return self.sub_scenarios

        def get_request(
            self, request_name: str
        ) -> "AsyncIntegrationTestStatus.AsyncRequestStatus":
            """
            Get request from the scenario
            """
            request_list = []
            for request in self.requests:
                if request.result_object.description.endswith("." + request_name):
                    request_list.append(request)
            if len(request_list) == 1:
                return request_list[0]
            # throw error that request not found
            if len(request_list) == 0:
                raise KeyError(f"Request {request_name} not found in the scenario")
            # throw error that multiple requests found
            if len(request_list) > 1:
                raise KeyError(
                    f"Multiple requests found with the name {request_name},please iterate over the requests"
                )
            return None

        def get_requests(self) -> List["AsyncIntegrationTestStatus.AsyncRequestStatus"]:
            """
            Get requests from the scenario
            """
            # sort the requests based on the id
            self.requests.sort(key=cmp_to_key(_sort_keys
            ))
            return self.requests

        def get_overall_status(self) -> Dict[str, str]:
            """
            Get overall status of the scenario
            """
            return {
                "name": self.name,
                "status": self.status,
                "error": self.error,
                "step_description": self.step_description,
                "step_name": self.step_name,
            }

        def assert_status(self) -> bool:
            """
            Assert the status of the scenario
            """
            return self.status

    class AsyncRequestStatus(BaseAsyncRequestStatus):
        """
        AsyncRequestStatus object
        """

        def __init__(self, result_object: dict):
            super().__init__(result_object)
            result_object = RawTestResult(result_object)
            self.result_object = result_object
            self.id = result_object.id
            self.name = result_object.description.split(".")[-1]

        def __repr__(self):
            # pylint: disable=line-too-long
            return f"AsyncRequestStatus(name={self.result_object.name}, status={self.result_object.status})"

        def get_response(self, json_path: str = None) -> str:
            output = ResponseLog(self.result_object.output)
            if output is None:
                return None
            return _get_response_value(output.payload, json_path)

        def get_var_value(self, key: str) -> str:
            state_object = TesterState(self.result_object.state)
            if state_object is not None:
                # check var in export ->vars ->scenario vars and return
                if (
                    key in state_object.exports
                    and state_object.exports[key] is not None
                ):
                    return state_object.exports[key]
                if key in state_object.vars and state_object.vars[key] is not None:
                    return state_object.vars[key]
                if (
                    key in state_object.scenario_vars
                    and state_object.scenario_vars[key] is not None
                ):
                    return state_object.scenario_vars[key]
            raise KeyError(f"Key {key} not found in the async data")

        def get_load_test_response(
            self, status_code: str, json_path: str = None
        ) -> str:
            raise NotImplementedError

    scenario_dict: Dict[str, AsyncScenarioStatus] = {}

    def __init__(self, options: dict):
        super().__init__(options)
        self.test_id = options.get("id", "")
        self.test_type = "integration"
        for result in options["results"][1:]:
            result_object = RawTestResult(result)
            if result_object.type == TestResultType.Scenario:
                self.scenario_dict[result_object.nested_info] = (
                    AsyncIntegrationTestStatus.AsyncScenarioStatus(result)
                )
                if result_object.parent is not None and result_object.parent != "":
                    if result_object.parent in self.scenario_dict:
                        self.scenario_dict[result_object.parent].sub_scenarios.append(
                            self.scenario_dict[result_object.nested_info]
                        )
            elif result_object.type == TestResultType.Request:
                if result_object.parent not in self.scenario_dict:
                    self.scenario_dict[result_object.parent] = (
                        AsyncIntegrationTestStatus.AsyncScenarioStatus(result)
                    )
                self.scenario_dict[result_object.parent].requests.append(
                    AsyncIntegrationTestStatus.AsyncRequestStatus(result)
                )

    def get_scenario(self, scenario_name) -> AsyncScenarioStatus:
        """
        Returns the scenario for the given scenario name
        """
        scenario_list = self.get_scenarios(scenario_name)
        if len(scenario_list) == 1:
            return scenario_list[0]
        # throw error that scenario not found
        if len(scenario_list) == 0:
            raise KeyError(f"Scenario {scenario_name} not found in the test")
        # throw error that multiple scenarios found
        if len(scenario_list) > 1:
            # pylint: disable=line-too-long
            raise KeyError(
                f"Multiple scenarios found with the name {scenario_name},please iterate over the scenarios"
            )
        return None

    def get_scenarios(self, scenario_name: str = "") -> List[AsyncScenarioStatus]:
        """
        Returns the scenarios
        """
        # sort the scenarios based on the id
        scenario_list = sorted(self.scenario_dict.values(), key=cmp_to_key(_sort_keys))
        if scenario_name == "":
            return list(scenario_list)
        scenarios = []
        # iterate over the scenario_dict and get scenario for the given scenario_name
        for scenario in scenario_list:
            # check scenario description ends with the scenario_name
            if scenario.name == scenario_name:
                scenarios.append(scenario)
        return scenarios

    def get_request(self, scenario_name: str, request_name: str) -> AsyncRequestStatus:
        """
        Returns the request for the given scenario name and request name
        """
        scenario = self.get_scenario(scenario_name)
        return scenario.get_request(request_name)

    def get_overall_status(self) -> Dict[str, str]:
        """
        Returns the overall status of the scenario
        """
        overall_status = []
        # iterate through top level scenarios and get the overall status
        for scenario_name, scenario in self.scenario_dict.items():
            if len(scenario_name.split(".")) == 2:
                overall_status.append(scenario.get_overall_status())
        return overall_status


@keyword
def log_load_metrics_to_robot(test_status: AsyncTestStatus):
    """Log to robot"""
    divider_text = "============================================================"
    request_divider_text = (
        "------------------------------------------------------------"
    )
    # log scenario request and response
    for scenario in test_status.get_scenarios(""):
        _log_data(divider_text)
        _log_data(
            f"<b>Scenario Name:</b> <span>{ scenario.name }</span>",
            html=True,
        )
        _log_data(
            f"<b>Stats:</b> { scenario.overall_status.to_json() }",
            html=True,
        )
        _log_data(divider_text)
        for request in scenario.get_requests():
            _log_data(f"<b>Request Name:</b> <span>{ request.name }</span>", html=True)
            _log_data(
                f"<b>Stats:</b> { request.result_object.get_stats() }",
                html=True,
            )
            _log_data(request_divider_text)
            _log_data(divider_text)
            # add divider to club status code and response for each request

            for status_code, json_data in request.result_object.log_table.items():
                json_data = json.loads(json_data)
                _log_data(
                    f"<b>Status Code:</b> <span>{ status_code }</span>",
                    html=True,
                )
                request = json_data.get("Request", None)
                if request is not None:
                    _log_data(
                        f"<b>Request:</b> <span>{ _sanitize_data(request) }</span>",
                        html=True,
                    )
                response = json_data.get("Response", None)
                if response is not None:
                    _log_data(
                        f"<b>Response:</b> <span>{ _sanitize_data(response) }</span>",
                        html=True,
                    )

                _log_data(divider_text)
            _log_data(request_divider_text)
        _log_data(divider_text)


def _sanitize_data(data: dict) -> dict:
    """
    Sanitize the data
    """
    # remove service object
    if "service" in data:
        data.pop("service")
    if "payload" in data:
        data["payload"] = sanitize_payload(data["payload"])
    if "headers" in data:
        data["headers"] = sanitize_headers_and_cookies(data["headers"])
    if "cookies" in data:
        data["cookies"] = sanitize_headers_and_cookies(data["cookies"])
    return data


def _log_data(text: str, html: bool = False):
    """Add divider"""
    BuiltIn().log(
        text,
        html=html,
        level="INFO",
    )


def _sort_keys(entry1, entry2) -> int:
    """
    Sort keys based on the provided logic.
    """
    entry1_list = entry1.id.split(".")
    entry2_list = entry2.id.split(".")

    for part1, part2 in zip(entry1_list, entry2_list):
        try:
            part1_num = int(part1[1:]) if part1[1:].isdigit() else part1
            part2_num = int(part2[1:]) if part2[1:].isdigit() else part2
        except ValueError:
            part1_num, part2_num = part1, part2

        if part1_num != part2_num:
            return -1 if part1_num < part2_num else 1

    # Compare lengths if all parts are equal
    return len(entry1_list) - len(entry2_list)
