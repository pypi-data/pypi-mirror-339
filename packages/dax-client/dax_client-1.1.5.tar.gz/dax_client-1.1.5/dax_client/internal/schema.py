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
from .misc import get_hostname
from .utils import get_username
from .setting import set_values


def init(name, version):
    """
    Initializes the schema by retrieving the hostname and username, 
    and setting the values for the package.

    Args:
        package_name (str): The name of the package to initialize.
        package_version (str): The version of the package to initialize.

    Returns:
        None
    """
    hname = get_hostname()
    uname = get_username()
    set_values(hname, uname, name, version)
