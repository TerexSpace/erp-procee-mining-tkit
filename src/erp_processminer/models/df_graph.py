"""
Defines the data structure for a Directly-Follows Graph (DFG).
"""

from typing import Tuple, Dict, Set
import networkx as nx

class DFG:
    """
    Represents a Directly-Follows Graph (DFG).

    The DFG is a directed graph where nodes are activities and edges
    represent that one activity was followed directly by another.
    Edge weights can represent frequency or performance metrics.
    """

    def __init__(self):
        self.graph: nx.DiGraph = nx.DiGraph()
        self.start_activities: Dict[str, int] = {}
        self.end_activities: Dict[str, int] = {}

    def add_activity(self, activity: str):
        """Adds an activity to the DFG if it doesn't already exist."""
        if not self.graph.has_node(activity):
            self.graph.add_node(activity, frequency=0)

    def add_edge(
        self, 
        source: str, 
        target: str, 
        weight: float = 1.0, 
        duration: float = 0.0
    ):
        """
        Adds or updates a directed edge between two activities.
        
        The 'frequency' attribute on the edge is incremented by `weight`.
        The 'total_duration' is updated to compute the average later.
        """
        if self.graph.has_edge(source, target):
            self.graph.edges[source, target]['frequency'] += weight
            self.graph.edges[source, target]['total_duration'] += duration
        else:
            self.graph.add_edge(
                source, 
                target, 
                frequency=weight, 
                total_duration=duration,
                avg_duration=0.0 # Will be computed later
            )
            
    def finalize(self):
        """
        Computes final metrics like average duration for all edges after
        the graph has been fully constructed.
        """
        for u, v, data in self.graph.edges(data=True):
            if data['frequency'] > 0:
                data['avg_duration'] = data['total_duration'] / data['frequency']

    def get_activities(self) -> Set[str]:
        """Returns the set of all activities in the DFG."""
        return set(self.graph.nodes)

    def get_edges(self) -> Dict[Tuple[str, str], Dict]:
        """Returns all edges with their attributes."""
        return {(u, v): d for u, v, d in self.graph.edges(data=True)}
        
    def __repr__(self) -> str:
        num_nodes = self.graph.number_of_nodes()
        num_edges = self.graph.number_of_edges()
        return f"DFG(nodes={num_nodes}, edges={num_edges})"