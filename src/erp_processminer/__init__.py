"""
ERP-ProcessMiner: A toolkit for process mining on ERP event logs
"""

__version__ = "0.1.0"

from .eventlog.structures import Event, Trace, EventLog
from .io_erp.loaders import load_erp_data
from .io_erp.mappings import apply_mapping

__all__ = [
    "Event",
    "Trace",
    "EventLog",
    "load_erp_data",
    "apply_mapping",
]