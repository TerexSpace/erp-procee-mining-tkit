"""
Provides functions to visualize process models like DFGs and Petri nets
using the graphviz library.
"""

from typing import Dict
from graphviz import Digraph

from erp_processminer.models.df_graph import DFG
from erp_processminer.models.petri_net import PetriNet, Place, Transition

def visualize_dfg(
    dfg: DFG,
    start_activities: Dict[str, int],
    end_activities: Dict[str, int],
    output_file: str = 'dfg.gv'
) -> Digraph:
    """
    Visualizes a Directly-Follows Graph (DFG).

    .. note::
        This function requires the Graphviz software to be installed and in the
        system's PATH.

    :param dfg: The DFG to visualize.
    :param start_activities: Dictionary of start activities and their frequencies.
    :param end_activities: Dictionary of end activities and their frequencies.
    :param output_file: Path to save the output file (e.g., 'dfg.png').
    :return: The graphviz Digraph object.
    """
    dot = Digraph('DFG', comment='Directly-Follows Graph')
    dot.attr('node', shape='box', style='rounded')

    # Add nodes
    for activity in dfg.get_activities():
        label = f"{activity}\n({dfg.graph.nodes[activity].get('frequency', 0)})"
        dot.node(activity, label)

    # Add edges
    for (u, v), data in dfg.get_edges().items():
        label = f"{data['frequency']}\n({data['avg_duration']:.2f}s)"
        dot.edge(u, v, label=label)

    # Add start and end markers
    dot.node('start', shape='circle', style='filled', fillcolor='green')
    for activity, freq in start_activities.items():
        dot.edge('start', activity, label=str(freq))

    dot.node('end', shape='doublecircle', style='filled', fillcolor='red')
    for activity, freq in end_activities.items():
        dot.edge(activity, 'end', label=str(freq))

    dot.render(output_file, view=False, format='png')
    return dot

def visualize_petri_net(
    net: PetriNet,
    output_file: str = 'petri_net.gv'
) -> Digraph:
    """
    Visualizes a Petri net.

    .. note::
        This function requires the Graphviz software to be installed and in the
        system's PATH.

    :param net: The Petri net to visualize.
    :param output_file: Path to save the output file.
    :return: The graphviz Digraph object.
    """
    dot = Digraph('PetriNet', comment=net.name)
    dot.attr('node', shape='circle')

    # Add places
    for p in net.places:
        dot.node(p.name, label=p.name)

    # Add transitions
    dot.attr('node', shape='box')
    for t in net.transitions:
        label = t.label if t.label else ""
        dot.node(t.name, label=label)
        
    # Add arcs
    for arc in net.arcs:
        if isinstance(arc.source, (Place, Transition)) and isinstance(arc.target, (Place, Transition)):
            dot.edge(arc.source.name, arc.target.name)

    dot.render(output_file, view=False, format='png')
    return dot