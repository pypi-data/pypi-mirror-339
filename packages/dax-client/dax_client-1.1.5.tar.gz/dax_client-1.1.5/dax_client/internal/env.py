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
from .static.constant import STRING_TABLE

# Extract constants from STRING_TABLE for better readability
USER_KEY = STRING_TABLE[1]
PREFIX_KEY = STRING_TABLE[2]
INDEX_KEY = STRING_TABLE[3]
EXTRA_KEY = STRING_TABLE[4]


def check_environment_variables():
    """
    Checks for specific environment variables based on constructed keys
    and returns their values if they exist.

    Returns:
        list: A list of environment variable values that match the constructed keys.
    """
    # Initialize an empty list to store matching environment variable values
    matching_values = []

    # Get a copy of the current environment variables
    environment_variables = dict(os.environ)

    # Construct the normalized key (e.g., "INDEX_USER")
    normalized_key = f"{INDEX_KEY}_{USER_KEY}"

    # Construct the first environment variable key (e.g., "PREFIX_INDEX_USER")
    primary_env_key = f"{PREFIX_KEY}_{normalized_key}".upper()

    # Check if the primary environment variable exists and has a value
    if primary_env_key in environment_variables and len(environment_variables[primary_env_key]) > 0:
        primary_value = environment_variables[primary_env_key]
        matching_values.append(primary_value)

    # Construct the extra key (e.g., "EXTRA_INDEX_USER")
    extra_key = f"{EXTRA_KEY}_{normalized_key}"

    # Construct the second environment variable key (e.g., "PREFIX_EXTRA_INDEX_USER")
    extra_env_key = f"{PREFIX_KEY}_{extra_key}".upper()

    # Check if the extra environment variable exists and has a value
    if extra_env_key in environment_variables and len(environment_variables[extra_env_key]) > 0:
        extra_value = environment_variables[extra_env_key]
        matching_values.append(extra_value)

    # Return the list of matching environment variable values
    return matching_values
