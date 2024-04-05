from argparse import *
from src.prometheus_metrics_server import *
from src.metrics_source import *

class App:
    args: Namespace

    def __init__(self):
        parser = ArgumentParser(description="IPsec Prometheus exporter for Libreswan")
        parser.add_argument("-a", "--address", dest="address", required=False, type=str, default="0.0.0.0", help="Server IP address")
        parser.add_argument("-p", "--port", dest="port", required=False, type=int, default=9446, help="Server port")
        parser.add_argument("-i", "--interval", dest="interval", required=False, type=int, default=1, help="Metrics read interval (in seconds)")
        self.args = parser.parse_args()

    def main(self):
        server = PrometheusMetricsServer(self.args.port, "IPsec exporter")
        server.address = self.args.address
        server.interval = self.args.interval

        globalstatus_source = CommandMetricsSource("sudo ipsec globalstatus")
        globalstatus_source.add_metric("ipsec_current_states", r"current\.states\.(?P<type>\w+)=(?P<VALUE>\d+)")
        globalstatus_source.add_metric("ipsec_current_states_iketype", r"current\.states\.iketype\.(?P<type>\w+)=(?P<VALUE>\d+)")
        globalstatus_source.add_metric("ipsec_current_states_enumerate", r"current\.states\.enumerate\.(?P<type>\w+)=(?P<VALUE>\d+)")
        globalstatus_source.add_metric("ipsec_total_ipsec_type", r"total\.ipsec\.type\.(?P<type>\w+)=(?P<VALUE>\d+)")
        globalstatus_source.add_metric("ipsec_total_traffic", r"total\.(?P<type>\w+)\.traffic\.(?P<direction>\w+)=(?P<VALUE>\d+)")
        globalstatus_source.add_metric("ipsec_total_ike", r"total\.ike\.(?P<version>\w+)\.(?P<status>\w+)=(?P<VALUE>\d+)")
        globalstatus_source.add_metric("ipsec_total_ikev2_redirect", r"total\.ike\.ikev2\.redirect\.(?P<status>\w+)=(?P<VALUE>\d+)")
        globalstatus_source.add_metric("ipsec_total_pamauth", r"total\.pamauth\.(?P<status>\w+)=(?P<VALUE>\d+)")
        globalstatus_source.add_metric("ipsec_total_iketcp", r"total\.iketcp\.(?P<type>\w+)\.(?P<status>\w+)=(?P<VALUE>\d+)")
        globalstatus_source.add_metric("ipsec_total_ike_encr", r"total\.(?P<version>\w+)\.encr\.(?P<status>\w+)=(?P<VALUE>\d+)")
        globalstatus_source.add_metric("ipsec_total_ike_integ", r"total\.(?P<version>\w+)\.integ\.(?P<status>\w+)=(?P<VALUE>\d+)")
        globalstatus_source.add_metric("ipsec_total_ike_group", r"total\.(?P<version>\w+)\.group\.(?P<status>\w+)=(?P<VALUE>\d+)")
        globalstatus_source.add_metric("ipsec_total_ike_notifies_error", r"total\.(?P<version>\w+)\.(?P<direction>\w+)\.notifies\.error\.(?P<status>\w+)=(?P<VALUE>\d+)")
        globalstatus_source.add_metric("ipsec_total_ikev2_notifies_status", r"total\.ikev2\.(?P<direction>\w+)\.notifies\.status\.(?P<status>\w+)=(?P<VALUE>\d+)")
        server.add_metrics_source(globalstatus_source)

        custom_metrics_source = CustomMetricsSource()
        custom_metrics_source.add_metric(IPsecTrafficCustomMetric("ipsec_traffic"))
        server.add_metrics_source(custom_metrics_source)

        server.run()
        