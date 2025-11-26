"""
Provides functions for analyzing process variants in an event log.
"""

from typing import List, Dict, Tuple
from collections import Counter
from erp_processminer.eventlog.structures import EventLog, Trace

def get_trace_variant(trace: Trace) -> Tuple[str, ...]:
    """
    Computes the variant of a single trace, which is the sequence of its
    activity names.

    :param trace: The trace to analyze.
    :return: A tuple of activity names representing the variant.
    """
    return tuple(event.activity for event in trace)

def get_variants(log: EventLog) -> Dict[Tuple[str, ...], List[Trace]]:
    """
    Identifies all process variants in an event log and groups traces by
    their variant.

    :param log: The event log to analyze.
    :return: A dictionary mapping each variant to a list of traces that
             follow that variant.
    """
    variants: Dict[Tuple[str, ...], List[Trace]] = {}
    for trace in log:
        variant = get_trace_variant(trace)
        if variant not in variants:
            variants[variant] = []
        variants[variant].append(trace)
    return variants

def get_variant_performance(log: EventLog) -> Dict[Tuple[str, ...], Dict]:
    """
    Calculates performance statistics for each process variant.

    :param log: The event log to analyze.
    :return: A dictionary mapping each variant to its performance stats
             (e.g., frequency, average cycle time).
    """
    from .performance import get_cycle_times
    
    variants = get_variants(log)
    variant_performance = {}
    
    for variant, traces in variants.items():
        cycle_times = get_cycle_times(EventLog(traces))
        
        avg_cycle_time = sum(cycle_times) / len(cycle_times) if cycle_times else 0
        
        variant_performance[variant] = {
            'frequency': len(traces),
            'avg_cycle_time': avg_cycle_time,
            'min_cycle_time': min(cycle_times) if cycle_times else 0,
            'max_cycle_time': max(cycle_times) if cycle_times else 0,
        }
        
    return variant_performance