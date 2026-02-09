from abc import ABC, abstractmethod
from metric import Metric, CommandMetric, CustomMetric
import os



class MetricsSource:
    _metrics : list[Metric]

    def __init__(self):
        self._metrics = []
    
    @abstractmethod
    def update(self):
        pass


class CommandMetricsSource(MetricsSource):
    command : str

    def __init__(self, command: str):
        super().__init__()
        self.command = command

    def add_metric(self, name: str, regex: str, description: str = ""):
        self._metrics.append(CommandMetric(name, regex, description))

    def update(self):
        output = os.popen(self.command).read()
        for metric in self._metrics:
            metric.update(output)


class CustomMetricsSource(MetricsSource):
    def __init__(self):
        super().__init__()
    
    def add_metric(self, custom_metric : CustomMetric):
        self._metrics.append(custom_metric)

    def update(self):
        for metric in self._metrics:
            metric.update()
