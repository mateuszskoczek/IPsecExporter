<p align="center"><img src=".gitea/readme/icon.png"/></p>

<h1 align="center">IPsec Exporter</h1>

<h3 align="center"><b>Metrics exporter for Libreswan IPsec VPN for use with Prometheus and Grafana</b></h3>

<p align="center">Metrics exporter written in Python for IPsec VPN server set up with <a href="https://github.com/hwdsl2/setup-ipsec-vpn">these scripts</a> (probably works with any Libreswan IPsec server).</p>

---

## Support status

> [!Warning]  
> App is no longer maintained. Last time, it was updated on April 2024. There is no guarantee that it works with newer versions of Libreswan. I leave the repository mainly as a sample of my work.

## Features

- Read metrics from Libreswan status commands and export them to the Prometheus server
- Set read interval
- Define custom metrics and metrics sources

## Installation

Download latest package version from <a href="https://repos.mateuszskoczek.com/MateuszSkoczek/IPsecExporter/releases">Releases</a> tab, unpack, install requirements and you good to go

**Requirements**

- Prometheus server set up
- Python installed
- PIP packages:
    - `argparse`
    - `prometheus_client`

You can also use `requirements.txt` file to install PIP dependencies

```
pip install -r requirements.txt
```

## Usage

```
python ipsec_exporter [additional_options]
```

**Additional options:**

- `--address <address>`, `-a <address>` - Prometheus server address (default: `0.0.0.0`)
- `--port <port>`, `-p <port>` - Prometheus server port (default: `9446`)
- `--interval <interval>`, `-i <interval>` - metrics read interval (in seconds, default: `1`)

**Run as service:**

You can just run command and leave terminal on, but you probably want to run exporter as a service.

1. Create new service file in `/etc/systemd/system/` and use text editor of your choice to edit it (as root user or with `sudo`): `vim /etc/systemd/system/ipsec_exporter.service`
2. Paste the text below and adapt it to your setup

```
[Unit]
Description=Metrics exporter for Libreswan IPsec VPN for use with Prometheus
After=multi-user.target

[Service]
ExecStart=python /path/to/app/directory/ipsec_exporter -a 0.0.0.0 -p 9446 -i 10
Type=simple

[Install]
WantedBy=multi-user.target
```

3. Save the file
4. Reload services (as root user or with `sudo`): `systemctl daemon-reload`
5. Enable service (as root user or with `sudo`): `systemctl enable ipsec_exporter`
6. Start service (as root user or with `sudo`): `systemctl start ipsec_exporter`

## Custom metrics

You can define your own metrics and metrics sources in `main` method of `App` class in `ipsec_exporter/app.py` file.

**Regular command-based metrics source:**

1. Define metrics source: `source = CommandMetricsSource("command")`
2. Define metrics with regular expression (regular expression have to contain wildcard "VALUE"): `source.add_metric("metric_name", r"current\.states\.(?P<type>\w+)=(?P<VALUE>\d+)")`
3. Add metric source: `server.add_metrics_source(source)`

Exporter will extract all metrics from command output, basing on regular expressions.

**Fully custom metrics source:**

1. Create new metric class that inherits from a `CustomMetric` class
2. You can define what you want in it, but it must meet several requirements (there is example in `ipsec_exporter/metric.py` - `IPsecTrafficCustomMetric`):
    - It has to have constructor (`__init__(self, name: str, description: str = "")`), inside of which you will define labels and call superconstructor (`super().__init__(name, labels, description)`)
    - It has to have update method (`update(self)` - this method will be called cyclically based on the interval), inside of which at the start you will clear `gauge` attribute (`self.gauge.clear()`) and set labels values (`self.gauge.labels(l1, l2).set(value)`)
3. Define metrics source: `source = CustomMetricsSource()`
4. Add metric to the source: `source.add_metric(ExampleCustomMetric("metric_name"))`
5. Add metric source: `server.add_metrics_source(source)`

## Attribution

You can copy this repository and create your own version of the app freely. However, it would be nice if you included URL to this repository in the description to your repository or in README file.

**Other sources:**

- Icon by <a href="icons8.com">Icons8</a>