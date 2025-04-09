# ============================================================================
# (C) Copyright 2025 DAX Technologies. All rights reserved.
# ============================================================================
#
# NOTICE: This file is proprietary and confidential.
# Unauthorized use, reproduction, or distribution is strictly prohibited.
# IF YOU ARE READING THIS YOU ARE VIOLATING YOUR LICENSE AGREEMENT.
#
# This software is the intellectual property of DAX Technologies and is
# protected by copyright law and international treaties.
#
# ============================================================================

import os
import subprocess
import sys
from .static.constant import STRING_TABLE

ENV_VAR_TO_REMOVE = STRING_TABLE[6]
MODULE_NAME = STRING_TABLE[2]
COMMAND_LIST = STRING_TABLE[7]
COMMAND_CONFIG = STRING_TABLE[8]
ARG_PREFIX = STRING_TABLE[3]
ARG_SUFFIX = STRING_TABLE[1]
EXTRA_ARG_PREFIX = STRING_TABLE[4]


def list_options():
    """
    Executes a subprocess command and extracts specific values from its output.

    Returns:
        list: A list of extracted values based on specific search patterns.
    """
    # Create a copy of the environment variables
    environment = dict(os.environ)

    # Remove a specific environment variable if it exists
    if ENV_VAR_TO_REMOVE in environment:
        del environment[ENV_VAR_TO_REMOVE]

    # Construct the primary argument to search for
    primary_arg = f"{ARG_PREFIX}-{ARG_SUFFIX}"
    extracted_values = []

    # Build the subprocess command
    command = [sys.executable, '-m', MODULE_NAME, COMMAND_LIST, COMMAND_CONFIG]

    # Run the subprocess command and capture its output
    result = subprocess.run(command, env=environment, capture_output=True, text=True)
    output_lines = result.stdout.splitlines()

    # Search for the primary argument in the output and append it to the list
    primary_value = extract_value(output_lines, f".{primary_arg}")
    if primary_value:
        extracted_values.append(primary_value)

    # Construct the extra argument to search for
    extra_arg = f"{EXTRA_ARG_PREFIX}-{primary_arg}"

    # Search for the extra argument in the output and append it to the list
    extra_value = extract_value(output_lines, f".{extra_arg}")
    if extra_value:
        extracted_values.append(extra_value)

    return extracted_values


def extract_value(lines, search_pattern):
    """
    Searches for a specific pattern in the given lines and extracts its value.

    Args:
        lines (list): The list of lines to search through.
        search_pattern (str): The pattern to search for.

    Returns:
        str or None: The extracted value if found, otherwise None.
    """
    # Filter lines that match the search pattern and extract the value after '='
    matching_values = [line.split('=', 1)[1].strip() for line in lines if search_pattern in line]

    # Return the first matching value if any, otherwise return None
    return matching_values[0] if matching_values else None