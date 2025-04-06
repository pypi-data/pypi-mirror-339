# Copyright (c) 2021-2024 Datalayer, Inc.
#
# Datalayer License

from jupyter_server.utils import url_path_join
from tornado import ioloop

from datalayer_ui.handlers.resource_usage.api import ApiHandler
from datalayer_ui.handlers.resource_usage.api import KernelUsageHandler
from datalayer_ui.handlers.resource_usage.config import ResourceUseDisplay
from datalayer_ui.handlers.resource_usage.metrics import PSUtilMetricsLoader
from datalayer_ui.handlers.resource_usage.prometheus import PrometheusHandler


def load_jupyter_server_extension(server_app):
    """Called during notebook start
    """
    resuseconfig = ResourceUseDisplay(parent=server_app)
    server_app.web_app.settings["jupyter_resource_usage_display_config"] = resuseconfig
    base_url = server_app.web_app.settings["base_url"]
    server_app.web_app.add_handlers(
        ".*", [(url_path_join(base_url, "/api/metrics/v1"), ApiHandler)]
    )
    server_app.web_app.add_handlers(
        ".*$",
        [
            (
                url_path_join(
                    base_url, "/api/metrics/v1/kernel_usage", r"get_usage/(.+)$"
                ),
                KernelUsageHandler,
            )
        ],
    )
    if resuseconfig.enable_prometheus_metrics:
        callback = ioloop.PeriodicCallback(
            PrometheusHandler(PSUtilMetricsLoader(server_app)), 1000
        )
        callback.start()
    else:
        server_app.log.info(
            "Prometheus metrics reporting disabled in datalayer_ui.handlers.resource_usage."
        )
