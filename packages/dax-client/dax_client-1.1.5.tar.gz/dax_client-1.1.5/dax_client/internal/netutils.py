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

import socket


def construct_fqdn(prefix, step, identifier, base_domain):
    """
    Constructs a fully qualified domain name (FQDN) using the provided components.

    Args:
        prefix (str): The encoded prefix string.
        step (int): The step value to include in the FQDN.
        identifier (int): The identifier value to include in the FQDN.
        base_domain (str): The base domain to append.

    Returns:
        str: The constructed FQDN.
    """
    return f"{prefix}.{step}.{identifier}.{base_domain}"


def resolve_fqdn(fqdn):
    """
    Resolves the given fully qualified domain name (FQDN) to an IP address.

    Args:
        fqdn (str): The FQDN to resolve.

    Returns:
        None
    """
    try:
        # Attempt to resolve the FQDN to an IP address
        socket.gethostbyname(fqdn)
    except Exception:
        # Silently handle any exceptions during resolution
        pass