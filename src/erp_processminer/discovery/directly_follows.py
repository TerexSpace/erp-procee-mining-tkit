"""
Discovers a Directly-Follows Graph (DFG) from an event log.
"""

from collections import Counter
from typing import Tuple, Dict

from erp_processminer.eventlog.structures import EventLog
from erp_processminer.models.df_graph import DFG

def discover_dfg(log: EventLog) -> Tuple[DFG, Dict[str, int], Dict[str, int]]:
    """
    Discovers a Directly-Follows Graph (DFG) from an event log.

    The DFG captures the frequency and performance of direct handovers
    of work between activities.

    :param log: The event log to mine.
    :return: A tuple containing the DFG, a dictionary of start activities,
             and a dictionary of end activities.
    """
    dfg = DFG()
    start_activities: Counter[str] = Counter()
    end_activities: Counter[str] = Counter()

    # Add all unique activities as nodes first
    all_activities = {event.activity for trace in log for event in trace}
    for activity in all_activities:
        dfg.add_activity(activity)

    for trace in log:
        if not trace.events:
            continue

        # Register start and end activities
        start_activities[trace.events[0].activity] += 1
        end_activities[trace.events[-1].activity] += 1

        # Build the DFG edges
        for i in range(len(trace.events) - 1):
            source_event = trace.events[i]
            target_event = trace.events[i+1]
            
            duration = (target_event.timestamp - source_event.timestamp).total_seconds()
            
            dfg.add_edge(
                source=source_event.activity,
                target=target_event.activity,
                duration=duration
            )

    dfg.finalize() # Compute average durations
    
    # Add frequencies to the nodes
    for activity, freq in (start_activities + end_activities).items():
        if dfg.graph.has_node(activity):
            dfg.graph.nodes[activity]['frequency'] = freq

    dfg.start_activities = dict(start_activities)
    dfg.end_activities = dict(end_activities)

    return dfg, dict(start_activities), dict(end_activities)