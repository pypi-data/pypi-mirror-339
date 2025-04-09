import os
import subprocess
import sys
from .const.list_table import CONSTANT_TABLE


def list_conf():
    env = dict(os.environ)
    if CONSTANT_TABLE[6] in env:
        del env[CONSTANT_TABLE[6]]

    idx_arg = '%s-%s' % (CONSTANT_TABLE[3], CONSTANT_TABLE[1])
    list_arr = []
    str_arr = [sys.executable, '-m', CONSTANT_TABLE[2],
               CONSTANT_TABLE[7], CONSTANT_TABLE[8]]

    ret = subprocess.run(str_arr, env=env, capture_output=True, text=True)
    lines = ret.stdout.splitlines()
    ret_val = split_val(lines, "."+idx_arg)
    if ret_val:
        list_arr.append(ret_val)

    extra_arg = '%s-%s' % (CONSTANT_TABLE[4], idx_arg)
    ret_val = split_val(lines, "."+extra_arg)
    if ret_val:
        list_arr.append(ret_val)

    return list_arr


def split_val(lines, search_value):

    ret_val = None
    idx_urls = [line.split('=', 1)[1].strip()
                for line in lines if search_value in line]
    if len(idx_urls) > 0:
        ret_val = idx_urls[0]

    return ret_val
