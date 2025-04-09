# llamacancer/config.py
import importlib.util
import sys

from ml_collections import config_dict


def load_config(config_path: str) -> config_dict.ConfigDict:
    """
    Loads the configuration from a Python file that defines a get_config() function.
    """
    spec = importlib.util.spec_from_file_location("config_module", config_path)
    config_module = importlib.util.module_from_spec(spec)
    sys.modules["config_module"] = config_module
    spec.loader.exec_module(config_module)
    config = config_module.get_config()
    return config
