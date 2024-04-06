from abc import abstractmethod
from prometheus_client import Gauge
from re import Pattern
import re
import os



class Metric:
    gauge: Gauge

    def __init__(self, name: str, labels: list[str], description: str = ""):
        self.gauge = Gauge(
            name,
            description,
            labels
        )


class CommandMetric(Metric):
    regex: Pattern

    def __init__(self, name: str, regex: str, description: str = ""):
        self.regex = re.compile(regex)

        labels = list(self.regex.groupindex.keys())
        labels.remove("VALUE")

        super().__init__(name, labels, description)

    def update(self, command_output: str):
        self.gauge.clear()

        results = re.finditer(self.regex, command_output)

        for result in results:
            groups = result.groupdict()
            value = groups.pop("VALUE")
            self.gauge.labels(*list(groups.values())).set(int(value))


class CustomMetric(Metric):
    def __init__(self, name: str, labels: list[str], description: str = ""):
        super().__init__(name, labels, description)

    @abstractmethod
    def update(self):
        pass


class IPsecTrafficCustomMetric(CustomMetric):
    def __init__(self, name: str, description: str = ""):
        labels = [
            "lease",
            "connection",
            "direction"
        ]
        super().__init__(name, labels, description)

    def update(self):
        self.gauge.clear()
        
        trafficstatus = os.popen("sudo ipsec trafficstatus").read()

        trafficstatus_results = re.finditer(r""""(?P<connection>.+)"\[\d+\] \d+\.\d+\.\d+\.\d+, type=\w+, add_time=\d+, inBytes=(?P<IN_VALUE>\d+), outBytes=(?P<OUT_VALUE>\d+), maxBytes=.+, id='.+', lease=(?P<lease>\d+\.\d+\.\d+\.\d+\/\d+)""", trafficstatus)

        for result in trafficstatus_results:
            lease = result.groupdict()["lease"]
            connection = result.groupdict()["connection"]
            in_value = result.groupdict()["IN_VALUE"]
            out_value = result.groupdict()["OUT_VALUE"]

            self.gauge.labels(lease, connection, "in").set(int(in_value))
            self.gauge.labels(lease, connection, "out").set(int(out_value))
