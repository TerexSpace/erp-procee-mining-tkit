"""
Provides functions for filtering event logs based on performance metrics
like cycle time.
"""
from erp_processminer.eventlog.structures import EventLog, Trace
from erp_processminer.statistics.performance import calculate_cycle_time

def filter_log_by_cycle_time(
    log: EventLog, 
    min_duration: float | None = None, 
    max_duration: float | None = None
) -> EventLog:
    """
    Filters an event log, keeping only traces with a cycle time within the
    specified range.

    :param log: The event log to filter.
    :param min_duration: The minimum cycle time in seconds.
    :param max_duration: The maximum cycle time in seconds.
    :return: A new, filtered EventLog.
    """
    new_traces = []
    for trace in log:
        cycle_time = calculate_cycle_time(trace)
        if cycle_time is None:
            continue

        if (min_duration is None or cycle_time >= min_duration) and \
           (max_duration is None or cycle_time <= max_duration):
            new_traces.append(trace)
            
    return EventLog(traces=new_traces)