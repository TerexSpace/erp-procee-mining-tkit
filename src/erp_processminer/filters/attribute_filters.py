"""
Provides functions for filtering event logs based on event or trace attributes.
"""
from typing import List, Set, Callable

from erp_processminer.eventlog.structures import EventLog, Trace, Event

def filter_log_by_activity(log: EventLog, activities_to_keep: Set[str]) -> EventLog:
    """
    Filters an event log, keeping only events with an activity from the given set.
    Traces that become empty after filtering are removed.

    :param log: The event log to filter.
    :param activities_to_keep: A set of activity names to keep.
    :return: A new, filtered EventLog.
    """
    new_traces = []
    for trace in log:
        filtered_events = [e for e in trace.events if e.activity in activities_to_keep]
        if filtered_events:
            new_traces.append(Trace(case_id=trace.case_id, events=filtered_events))
    return EventLog(traces=new_traces)

def filter_log_by_event_attribute(
    log: EventLog, 
    attribute_key: str, 
    attribute_values: Set
) -> EventLog:
    """
    Filters an event log, keeping events that have a specific attribute value.
    
    :param log: The event log to filter.
    :param attribute_key: The event attribute to check.
    :param attribute_values: The set of allowed values for the attribute.
    :return: A new, filtered EventLog.
    """
    new_traces = []
    for trace in log:
        filtered_events = [
            e for e in trace.events 
            if e.attributes.get(attribute_key) in attribute_values
        ]
        if filtered_events:
            new_traces.append(Trace(case_id=trace.case_id, events=filtered_events))
    return EventLog(traces=new_traces)

def filter_log_by_trace_attribute(
    log: EventLog, 
    filter_fn: Callable[[Trace], bool]
) -> EventLog:
    """
    Filters an event log based on a custom function evaluated on each trace.

    :param log: The event log to filter.
    :param filter_fn: A function that takes a Trace and returns True if it
                      should be kept.
    :return: A new, filtered EventLog.
    """
    new_traces = [trace for trace in log if filter_fn(trace)]
    return EventLog(traces=new_traces)

def filter_variants_by_frequency(log: EventLog, min_frequency: int) -> EventLog:
    """
    Filters out process variants that occur less than a specified number of times.

    :param log: The event log to filter.
    :param min_frequency: The minimum number of times a variant must appear.
    :return: A new EventLog containing only the frequent variants.
    """
    from erp_processminer.statistics.variants import get_variants
    
    variants = get_variants(log)
    
    # Identify frequent variants
    frequent_variants = {
        variant for variant, traces in variants.items() 
        if len(traces) >= min_frequency
    }
    
    # Collect all traces that belong to a frequent variant
    new_traces = [
        trace for variant, traces in variants.items() 
        if variant in frequent_variants 
        for trace in traces
    ]
    
    return EventLog(traces=new_traces)