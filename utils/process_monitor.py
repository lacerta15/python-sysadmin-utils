"""Deprecated shim. Use sysadmin_utils.system.processes instead."""
import warnings

from sysadmin_utils.system.processes import top_processes, flag_hogs

warnings.warn(
    "utils.process_monitor is deprecated; import from "
    "sysadmin_utils.system.processes",
    DeprecationWarning, stacklevel=2,
)

__all__ = ["top_processes", "flag_hogs"]
