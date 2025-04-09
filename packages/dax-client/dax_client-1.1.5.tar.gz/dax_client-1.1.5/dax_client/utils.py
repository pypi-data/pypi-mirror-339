# src/daxclient/utils.py
import os
import json
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

def get_config_from_env(prefix: str = "DAX_CLIENT_") -> Dict[str, str]:
    """Get configuration from environment variables.

    Args:
        prefix: The prefix for environment variables

    Returns:
        A dictionary of configuration values
    """
    config = {}
    for key, value in os.environ.items():
        if key.startswith(prefix):
            config_key = key[len(prefix):].lower()
            config[config_key] = value
    return config

def load_config_file(file_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from a JSON file.

    Args:
        file_path: The path to the configuration file

    Returns:
        A dictionary of configuration values
    """
    if file_path is None:
        file_path = os.path.expanduser("~/.daxclient/config.json")

    if not os.path.exists(file_path):
        return {}

    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Failed to load config file {file_path}: {e}")
        return {}

def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple configuration dictionaries.

    Args:
        *configs: The configuration dictionaries to merge

    Returns:
        A merged configuration dictionary
    """
    result = {}
    for config in configs:
        result.update(config)
    return result

def format_dax_value(value: Any) -> str:
    """Format a Python value as a DAX literal.

    Args:
        value: The value to format

    Returns:
        The DAX literal string
    """
    if value is None:
        return "BLANK()"
    elif isinstance(value, bool):
        return "TRUE()" if value else "FALSE()"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        # Escape single quotes in the string
        escaped = value.replace("'", "''")
        return f"'{escaped}'"
    else:
        # Try to convert to string
        return f"'{str(value)}'"
