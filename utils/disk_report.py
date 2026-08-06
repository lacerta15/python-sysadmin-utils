"""Deprecated shim. Use sysadmin_utils.system.disk instead."""
import warnings

from sysadmin_utils.system.disk import report, remote_usage, local_usage

warnings.warn(
    "utils.disk_report is deprecated; import from sysadmin_utils.system.disk",
    DeprecationWarning, stacklevel=2,
)

__all__ = ["report", "remote_usage", "local_usage"]
