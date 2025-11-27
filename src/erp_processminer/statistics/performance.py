"""
Provides functions for calculating performance-related statistics on
event logs, such as cycle times and waiting times.
"""

from typing import List, Dict, Tuple
from erp_processminer.eventlog.structures import EventLog, Trace, Event

def calculate_cycle_time(trace: Trace) -> float | None:
    """
    Calculates the cycle time of a single trace (duration from the first
    to the last event).

    :param trace: The trace to analyze.
    :return: The cycle time in seconds, or None if the trace is empty.
    """
    if len(trace.events) < 1:
        return None
    
    start_time = trace.events[0].timestamp
    end_time = trace.events[-1].timestamp
    
    return (end_time - start_time).total_seconds()

def get_cycle_times(log: EventLog) -> List[float]:
    """
    Calculates the cycle time for every trace in an event log.

    :param log: The event log to analyze.
    :return: A list of cycle times in seconds.
    """
    cycle_times = []
    for trace in log:
        ct = calculate_cycle_time(trace)
        if ct is not None:
            cycle_times.append(ct)
    return cycle_times

def calculate_waiting_times(trace: Trace) -> Dict[Tuple[str, str], List[float]]:
    """
    Calculates the waiting time between all directly-following activities
    in a trace.

    :param trace: The trace to analyze.
    :return: A dictionary mapping activity pairs to a list of waiting times.
    """
    waiting_times = {}
    for i in range(len(trace.events) - 1):
        source_event = trace.events[i]
        target_event = trace.events[i+1]
        
        pair = (source_event.activity, target_event.activity)
        duration = (target_event.timestamp - source_event.timestamp).total_seconds()
        
        if pair not in waiting_times:
            waiting_times[pair] = []
        waiting_times[pair].append(duration)
        
    return waiting_times

def get_all_waiting_times(log: EventLog) -> Dict[Tuple[str, str], List[float]]:
    """
    Aggregates waiting times across all traces in an event log.

    :param log: The event log to analyze.
    :return: A dictionary mapping activity pairs to a list of all observed
             waiting times.
    """
    all_waiting_times = {}
    for trace in log:
        trace_waiting_times = calculate_waiting_times(trace)
        for pair, durations in trace_waiting_times.items():
            if pair not in all_waiting_times:
                all_waiting_times[pair] = []
            all_waiting_times[pair].extend(durations)
            
    return all_waiting_times
