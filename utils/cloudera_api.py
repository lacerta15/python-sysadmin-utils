"""Deprecated shim. Use sysadmin_utils.cloud.cloudera instead."""
import warnings

from sysadmin_utils.cloud.cloudera import ClouderaClient

warnings.warn(
    "utils.cloudera_api is deprecated; import from "
    "sysadmin_utils.cloud.cloudera",
    DeprecationWarning, stacklevel=2,
)

__all__ = ["ClouderaClient"]
