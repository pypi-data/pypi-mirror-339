"""A helper CLI for Netflix Open Content media."""

import importlib.metadata
import os

import yaml

__version__ = importlib.metadata.version(__package__)

package_dir = os.path.dirname(__file__)
config_file = os.path.join(package_dir, "config", "config.yaml")

# Check if the config file exists
if not os.path.exists(config_file):
    raise FileNotFoundError(f"Configuration file not found: {config_file}")
# Load the configuration file
with open(config_file) as file:
    CONFIG = yaml.safe_load(file)
