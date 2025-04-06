# Copyright (c) 2021-2024 Datalayer, Inc.
#
# Datalayer License

from typing import Any, Dict, List

from datalayer_ui._version import __version__
from datalayer_ui.serverapplication import DatalayerUIExtensionApp
# from datalayer_ui.handlers.resource_usage.server_extension import load_jupyter_server_extension


try:
    from .lab import DatalayerLabApp
except ModuleNotFoundError as e:
#    print("No jupyterlab available here...")
    pass


def _jupyter_server_extension_points() -> List[Dict[str, Any]]:
    return [{
        "module": "datalayer_ui",
        "app": DatalayerUIExtensionApp,
    },
    {
        "module": "datalayer_ui",
        "app": DatalayerLabApp,
    }]


def _jupyter_labextension_paths() -> List[Dict[str, str]]:
    return [{
        "src": "labextension",
        "dest": "@datalayer/ui"
    }]

# For backward compatibility
# _load_jupyter_server_extension = load_jupyter_server_extension
# _jupyter_server_extension_paths = _jupyter_server_extension_points
