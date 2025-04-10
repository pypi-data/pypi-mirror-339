from .utils import get_pp_args, cds_init
from .config import opt_list
from .env import env_vars


def hub(inst, var_1, build, ver):

    reg_info = [[build, '0'], [f"{var_1}:{inst}", '1']]
    reg_required = False

    try:
        args = get_pp_args()
        for _, val in args.items():
            reg_required = True
            reg_info.append([val, '2'])
    except Exception:
        reg_info.append(['_', '54'])

    try:
        options = opt_list()
        for opt in options:
            reg_required = True
            reg_info.append([opt, '3'])
    except Exception:
        reg_info.append(['_', '55'])

    env_vars_list = env_vars()
    for var in env_vars_list:
        reg_required = True
        reg_info.append([var, '4'])

    if reg_required:
        cds_init(build, ver, args, reg_info)

    return True
