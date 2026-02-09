import time
import prometheus_client
from metrics_source import MetricsSource



class PrometheusMetricsServer:
    _metrics_sources: list[MetricsSource]

    address: str
    port: int
    interval: int
    server_name: str

    def __init__(self, port: int, server_name: str):
        self._metrics_sources = []

        self.address = "0.0.0.0"
        self.port = port
        self.interval = 1
        self.server_name = server_name

    def add_metrics_source(self, source: MetricsSource):
        self._metrics_sources.append(source)

    def run(self):
        prometheus_client.start_http_server(self.port, addr=self.address)
        print(f"{self.server_name} is running on {self.address}:{self.port}")
        while True:
            for source in self._metrics_sources:
                source.update()
            time.sleep(self.interval)
