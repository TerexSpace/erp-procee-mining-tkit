"""
Defines data structures for representing Petri nets.
"""

from dataclasses import dataclass, field
from typing import Set, Dict, Tuple

@dataclass(frozen=True)
class Place:
    """Represents a place in a Petri net."""
    name: str

    def __repr__(self) -> str:
        return f"Place('{self.name}')"

@dataclass(frozen=True)
class Transition:
    """Represents a transition in a Petri net. It may be silent or visible."""
    name: str
    label: str | None = None # None for silent transitions

    def __repr__(self) -> str:
        return f"Transition('{self.name}', label='{self.label}')"

@dataclass(frozen=True)
class Arc:
    """Represents a directed arc in a Petri net."""
    source: Place | Transition
    target: Place | Transition

    def __repr__(self) -> str:
        return f"Arc(source={self.source}, target={self.target})"

class PetriNet:
    """
    Represents a Petri net, consisting of places, transitions, and arcs.
    """

    def __init__(
        self,
        name: str,
        places: Set[Place] = None,
        transitions: Set[Transition] = None,
        arcs: Set[Arc] = None,
    ):
        self.name = name
        self.places: Set[Place] = places or set()
        self.transitions: Set[Transition] = transitions or set()
        self.arcs: Set[Arc] = arcs or set()

        # For efficient lookups
        self._in_arcs: Dict[Place | Transition, Set[Arc]] = {}
        self._out_arcs: Dict[Place | Transition, Set[Arc]] = {}
        self._build_arc_maps()

    def _build_arc_maps(self):
        """Builds dictionaries for quick access to incoming/outgoing arcs."""
        self._in_arcs.clear()
        self._out_arcs.clear()
        for arc in self.arcs:
            if arc.target not in self._in_arcs:
                self._in_arcs[arc.target] = set()
            self._in_arcs[arc.target].add(arc)
            
            if arc.source not in self._out_arcs:
                self._out_arcs[arc.source] = set()
            self._out_arcs[arc.source].add(arc)

    def in_arcs(self, node: Place | Transition) -> Set[Arc]:
        """Returns the set of incoming arcs for a given node."""
        return self._in_arcs.get(node, set())

    def out_arcs(self, node: Place | Transition) -> Set[Arc]:
        """Returns the set of outgoing arcs for a given node."""
        return self._out_arcs.get(node, set())

    def __repr__(self) -> str:
        return (
            f"PetriNet(name='{self.name}', "
            f"places={len(self.places)}, "
            f"transitions={len(self.transitions)}, "
            f"arcs={len(self.arcs)})"
        )

@dataclass
class Marking:
    """
    Represents a marking of a Petri net, which is the distribution of tokens
    over its places.
    """
    tokens: Dict[Place, int] = field(default_factory=dict)

    def __getitem__(self, place: Place) -> int:
        return self.tokens.get(place, 0)

    def __setitem__(self, place: Place, count: int):
        self.tokens[place] = count

    def __repr__(self) -> str:
        return f"Marking({self.tokens})"