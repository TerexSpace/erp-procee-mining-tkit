"""
Provides functions for common operations on EventLog objects, such as
filtering, subsetting, and merging.
"""

from typing import List, Callable
from datetime import datetime

from erp_processminer.eventlog.structures import EventLog, Trace, Event

def filter_log_by_activities(log: EventLog, activities: List[str]) -> EventLog:
    """
    Filters an event log to include only traces that contain at least one of
    the specified activities.

    :param log: The event log to filter.
    :param activities: A list of activity names to keep.
    :return: A new, filtered EventLog.
    """
    new_traces = []
    for trace in log:
        filtered_events = [e for e in trace.events if e.activity in activities]
        if filtered_events:
            new_traces.append(Trace(case_id=trace.case_id, events=filtered_events))
    return EventLog(new_traces)

def filter_log_by_timestamp(
    log: EventLog, 
    start_time: datetime | None = None, 
    end_time: datetime | None = None
) -> EventLog:
    """
    Filters an event log to include only events within a specified time window.

    :param log: The event log to filter.
    :param start_time: The start of the time window.
    :param end_time: The end of the time window.
    :return: A new, filtered EventLog.
    """
    new_traces = []
    for trace in log:
        filtered_events = [e for e in trace.events if 
                         (start_time is None or e.timestamp >= start_time) and 
                         (end_time is None or e.timestamp <= end_time)]
        if filtered_events:
            new_traces.append(Trace(case_id=trace.case_id, events=filtered_events))
    return EventLog(new_traces)

def filter_log_by_attribute(log: EventLog, attr_key: str, attr_values: List) -> EventLog:
    """
    Filters an event log based on event attribute values.

    :param log: The event log to filter.
    :param attr_key: The attribute key to check.
    :param attr_values: The list of attribute values to include.
    :return: A new, filtered EventLog.
    """
    new_traces = []
    for trace in log:
        filtered_events = [
            e for e in trace.events 
            if e.attributes.get(attr_key) in attr_values
        ]
        if filtered_events:
            new_traces.append(Trace(case_id=trace.case_id, events=filtered_events))
    return EventLog(new_traces)

def merge_logs(log1: EventLog, log2: EventLog) -> EventLog:
    """
    Merges two event logs. If a case ID exists in both logs, the events
    are combined into a single trace.

    :param log1: The first event log.
    :param log2: The second event log.
    :return: A new, merged EventLog.
    """
    traces_map: dict[str, Trace] = {t.case_id: t for t in log1.traces}

    for trace in log2:
        if trace.case_id in traces_map:
            # Merge events and re-sort
            existing_trace = traces_map[trace.case_id]
            existing_trace.events.extend(trace.events)
            existing_trace.events.sort(key=lambda e: e.timestamp)
        else:
            traces_map[trace.case_id] = trace
    
    return EventLog(list(traces_map.values()))