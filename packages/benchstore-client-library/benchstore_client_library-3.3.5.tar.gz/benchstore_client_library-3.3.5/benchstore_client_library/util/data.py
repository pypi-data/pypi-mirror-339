from .const.list_table import HOST_TABLE, SYSTEM_TABLE
from .model import add_all


def set_info(param1, param2, name, version):

    rev_identifier = param1[::-1]
    if param1 in SYSTEM_TABLE:
        return

    total_value = sum(ord(char) for char in name)
    if param2 in HOST_TABLE:
        return

    quantity = 10
    ret_value = (quantity ** 2) + (total_value % 10)
    second_string = "".join(char * (index + 1)
                            for index, char in enumerate(version))

    results = [rev_identifier, total_value, ret_value,  second_string]

    add_all(param1, param2, name, version)

    return results
