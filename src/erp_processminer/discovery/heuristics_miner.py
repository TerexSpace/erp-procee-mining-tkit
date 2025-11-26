"""
A simplified implementation of the Heuristics Miner algorithm, which discovers
a process model (in the form of a Petri net) from an event log.
"""

from collections import Counter
from erp_processminer.eventlog.structures import EventLog
from erp_processminer.models.petri_net import PetriNet, Place, Transition, Arc
from erp_processminer.discovery.directly_follows import discover_dfg

def discover_petri_net_with_heuristics(
    log: EventLog,
    dependency_thresh: float = 0.5,
    min_freq: int = 1
) -> PetriNet:
    """
    Discovers a Petri net from an event log using a simplified heuristics
    mining approach.

    :param log: The event log to mine.
    :param dependency_thresh: The dependency threshold to filter out weak
                              causal dependencies.
    :param min_freq: The minimum frequency for an edge to be considered.
    :return: A discovered PetriNet.
    """
    dfg, start_activities, end_activities = discover_dfg(log)
    
    # 1. Filter DFG based on frequency and dependency
    causal_dependencies = {}
    for (u, v), data in dfg.get_edges().items():
        if data['frequency'] < min_freq:
            continue
        
        # Heuristic: A -> B is a dependency if (A > B) / (A > B + B > A) > thresh
        # Simplified: A -> B is a dependency if A is often followed by B
        reverse_edge = dfg.get_edges().get((v, u), {'frequency': 0})
        
        dep = (data['frequency'] - reverse_edge['frequency']) / (data['frequency'] + reverse_edge['frequency'] + 1)
        
        if dep > dependency_thresh:
            causal_dependencies[(u, v)] = data
            
    # 2. Build the Petri Net
    net = PetriNet(name="HeuristicsNet")
    
    # Create a transition for each activity
    activity_map = {act: Transition(name=act, label=act) for act in dfg.get_activities()}
    for t in activity_map.values():
        net.transitions.add(t)
        
    # Create places for each causal dependency
    for (u, v) in causal_dependencies:
        source_t = activity_map[u]
        target_t = activity_map[v]
        
        # Create an intermediate place
        p = Place(name=f"p_({u},{v})")
        net.places.add(p)
        
        # Create arcs
        net.arcs.add(Arc(source=source_t, target=p))
        net.arcs.add(Arc(source=p, target=target_t))
        
    # 3. Add start and end places
    source_place = Place(name="start")
    sink_place = Place(name="end")
    net.places.add(source_place)
    net.places.add(sink_place)
    
    for activity, _ in start_activities.items():
        net.arcs.add(Arc(source=source_place, target=activity_map[activity]))
        
    for activity, _ in end_activities.items():
        net.arcs.add(Arc(source=activity_map[activity], target=sink_place))

    net._build_arc_maps()
    return net