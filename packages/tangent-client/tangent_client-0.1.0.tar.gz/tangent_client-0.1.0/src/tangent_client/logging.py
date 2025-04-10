"""tangent_client.logging."""

import contextlib
import importlib
import logging

import libranet_logging

log = logging.getLogger(__name__)
julia_core_log = logging.getLogger("tangent_julia_core")


def initialize() -> None:
    """Configure logging using the logging.yaml file from the package resources."""
    logging_yaml_file = importlib.resources.files("tangent_client").joinpath("logging.yaml")  # Python3.9+
    libranet_logging.initialize(path=logging_yaml_file)
