"""Get config directories."""

import os
import appdirs
from .__version__ import __app_name__, __author_name__


def get_config_dir():
    """Get config directory.

    Returns:
        config_dir
    """
    config_dir = appdirs.user_config_dir(__app_name__, __author_name__)
    return config_dir


def get_data_dir():
    """Get data directory.

    Returns:
        data_dir
    """
    data_dir = appdirs.user_data_dir(__app_name__, __author_name__)
    return data_dir


def get_probe_dir():
    """Get probe dir.

    Returns:
        probe_dir
    """
    data_dir = get_data_dir()
    probe_dir = os.path.join(data_dir, "ffprobe_data")
    os.makedirs(probe_dir, mode=0o750, exist_ok=True)
    return probe_dir



