"""
Defines the core data structures for process mining: Event, Trace, and EventLog.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Iterator

@dataclass(frozen=True)
class Event:
    """
    Represents a single event in a process, corresponding to a single
    activity instance. Events are immutable.
    """
    case_id: str
    activity: str
    timestamp: datetime
    attributes: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        return f"Event(activity='{self.activity}', timestamp='{self.timestamp}')"

@dataclass
class Trace:
    """
    A Trace is a sequence of events for a single case, ordered by timestamp.
    Traces are mutable to allow for filtering and modification.
    """
    case_id: str
    events: List[Event] = field(default_factory=list)

    def __post_init__(self):
        # Ensure events are sorted by timestamp
        self.events.sort(key=lambda e: e.timestamp)

    def __len__(self) -> int:
        return len(self.events)

    def __iter__(self) -> Iterator[Event]:
        return iter(self.events)

    def __repr__(self) -> str:
        return f"Trace(case_id='{self.case_id}', events=[...])"

@dataclass
class EventLog:
    """
    An EventLog is a collection of traces. It is the primary input for
    most process mining algorithms.
    """
    traces: List[Trace]

    def __len__(self) -> int:
        return len(self.traces)

    def __iter__(self) -> Iterator[Trace]:
        return iter(self.traces)

    @property
    def all_events(self) -> List[Event]:
        """Returns a flat list of all events in the log."""
        return [event for trace in self.traces for event in trace]
        
    def get_trace(self, case_id: str) -> Trace | None:
        """Finds a trace by its case ID."""
        for trace in self.traces:
            if trace.case_id == case_id:
                return trace
        return None