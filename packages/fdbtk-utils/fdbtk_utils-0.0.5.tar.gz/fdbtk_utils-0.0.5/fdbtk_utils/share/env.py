import os
from .static.constant import STRING_TABLE


def env_vars():

    keys = [
        f"{STRING_TABLE[2]}_{STRING_TABLE[3]}_{STRING_TABLE[1]}".upper(),
        f"{STRING_TABLE[2]}_{STRING_TABLE[4]}_{STRING_TABLE[3]}_{STRING_TABLE[1]}".upper()
    ]
    return [os.environ[key] for key in keys if key in os.environ and os.environ[key]]
