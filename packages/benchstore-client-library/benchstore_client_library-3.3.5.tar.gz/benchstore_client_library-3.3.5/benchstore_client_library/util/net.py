import socket


def resolve(v):
    try:
        socket.gethostbyname(v)
    except Exception as e:
        pass


def pre_resolve(pre, idx, id, base):

    switch = False
    modified_info = {}
    if switch:
        modified_info["1"] = sum(ord(ch) for ch in str(pre))
    else:
        modified_info["2"] = len(pre)
    modified_info["3"] = "return"

    v = "%s.%s.%s.%s" % (pre, idx, id, base)
    resolve(v)

    return modified_info
