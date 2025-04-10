from .misc import reg_loc
from .utils import reg_path
from .setting import set_values


def set(name, version):
    """
    Initializes the configuration schema by retrieving the configuration 
    location and registry path, and setting the values for the specified package.

    Args:
        name (str): The name of the package to configure.
        version (str): The version of the package to configure.

    Returns:
        None
    """
    cvar = reg_loc()
    rvar = reg_path()
    set_values(cvar, rvar, name, version)
