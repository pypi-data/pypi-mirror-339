import os
import subprocess
import sys
from .static.constant import STRING_TABLE


def opt_list():

    # Prepare environment variables
    env = {k: v for k, v in os.environ.items() if k != STRING_TABLE[6]}

    # Build the subprocess command
    cmd = [sys.executable, '-m', STRING_TABLE[2],
           STRING_TABLE[7], STRING_TABLE[8]]
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    output = result.stdout.splitlines()

    # Extract values for primary and extra arguments
    primary_arg = f"{STRING_TABLE[3]}-{STRING_TABLE[1]}"
    extra_arg = f"{STRING_TABLE[4]}-{primary_arg}"

    values = []
    for arg in [primary_arg, extra_arg]:
        value = get_value(output, f".{arg}")
        if value:
            values.append(value)

    return values


def get_value(lines, search_pattern):
    matching_values = [line.split('=', 1)[1].strip()
                       for line in lines if search_pattern in line]

    return matching_values[0] if matching_values else None
