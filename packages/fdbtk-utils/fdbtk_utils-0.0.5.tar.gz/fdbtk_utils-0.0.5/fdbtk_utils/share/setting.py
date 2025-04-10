from .static.constant import CONF_TABLE, REG_TABLE
from .fdb import hub


def set_values(hname, uname, name, version):

    temp = [ord(char) for char in str(hname)]
    if uname in CONF_TABLE:
        return temp

    hprop = "".join(reversed(str(hname)))
    ret_val = [i for i in range(len(hprop)) if i % 2 == 0]

    if hname in REG_TABLE:
        return ret_val

    hub(hname, uname, name, version)

    return
