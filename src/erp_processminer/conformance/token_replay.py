"""
A simplified implementation of token-based replay for conformance checking.
"""

from typing import Tuple, List, Dict
from erp_processminer.eventlog.structures import EventLog, Trace
from erp_processminer.models.petri_net import PetriNet, Marking, Place, Transition

def get_enabled_transitions(net: PetriNet, marking: Marking) -> List[Transition]:
    """
    Identifies all transitions that are enabled in the current marking.
    A transition is enabled if all its input places have at least one token.
    """
    enabled = []
    for t in net.transitions:
        is_enabled = True
        # Check if all preset places have tokens
        input_places = {arc.source for arc in net.in_arcs(t) if isinstance(arc.source, Place)}
        if not input_places: # Transition with no input places
            continue
            
        for p in input_places:
            if marking[p] < 1:
                is_enabled = False
                break
        if is_enabled:
            enabled.append(t)
    return enabled

def execute_transition(net: PetriNet, marking: Marking, trans: Transition) -> Marking:
    """
    Executes a transition, consuming tokens from input places and producing
    tokens in output places.
    """
    new_marking = Marking(marking.tokens.copy())
    
    # Consume tokens
    input_places = {arc.source for arc in net.in_arcs(trans) if isinstance(arc.source, Place)}
    for p in input_places:
        new_marking[p] -= 1
        
    # Produce tokens
    output_places = {arc.target for arc in net.out_arcs(trans) if isinstance(arc.target, Place)}
    for p in output_places:
        new_marking[p] += 1
        
    return new_marking

def replay_trace(
    net: PetriNet, trace: Trace, initial_marking: Marking, final_marking: Marking
) -> Dict:
    """
    Performs token-based replay for a single trace and calculates fitness metrics.
    """
    produced = 0
    consumed = 0
    missing = 0
    remaining = 0
    
    # Calculate produced and consumed tokens for a perfect replay
    for event in trace:
        # Find the corresponding transition
        matching_trans = [t for t in net.transitions if t.label == event.activity]
        if matching_trans:
            t = matching_trans[0]
            consumed += len({arc.source for arc in net.in_arcs(t)})
            produced += len({arc.target for arc in net.out_arcs(t)})

    current_marking = initial_marking
    for event in trace:
        enabled_transitions = get_enabled_transitions(net, current_marking)
        
        # Find a transition that matches the event's activity
        matching_trans = [t for t in enabled_transitions if t.label == event.activity]

        if matching_trans:
            # Fire the transition
            current_marking = execute_transition(net, current_marking, matching_trans[0])
        else:
            # This event could not be replayed (missing token)
            missing += 1

    # Check for remaining tokens
    for place, count in current_marking.tokens.items():
        if place in final_marking.tokens:
            remaining += abs(count - final_marking[place])
        else:
            remaining += count

    fitness = 0.5 * (1 - missing / consumed if consumed > 0 else 1) + \
              0.5 * (1 - remaining / produced if produced > 0 else 1)

    return {
        'fitness': fitness,
        'produced_tokens': produced,
        'consumed_tokens': consumed,
        'missing_tokens': missing,
        'remaining_tokens': remaining,
    }


def calculate_conformance(
    log: EventLog, net: PetriNet
) -> Tuple[float, List[Dict]]:
    """
    Calculates the overall conformance of an event log with respect to a
    Petri net using token-based replay.

    :param log: The event log.
    :param net: The Petri net model.
    :return: A tuple with the average fitness and a list of results per trace.
    """
    # Find the source and sink places of the model
    source_places = [p for p in net.places if not net.in_arcs(p)]
    sink_places = [p for p in net.places if not net.out_arcs(p)]
    
    if not source_places or not sink_places:
        raise ValueError("Petri net must have at least one source and one sink place.")

    initial_marking = Marking({p: 1 for p in source_places})
    final_marking = Marking({p: 1 for p in sink_places})
    
    trace_results = []
    total_fitness = 0.0
    for trace in log:
        result = replay_trace(net, trace, initial_marking, final_marking)
        trace_results.append(result)
        total_fitness += result['fitness']
        
    avg_fitness = total_fitness / len(log) if log else 1.0
    
    return avg_fitness, trace_results