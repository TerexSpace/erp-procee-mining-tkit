"""
Tests for the core event log data structures.
"""

import pytest
from datetime import datetime
from erp_processminer.eventlog.structures import Event, Trace, EventLog

def test_event_creation():
    """Tests the creation of an Event object."""
    now = datetime.now()
    event = Event(
        case_id="C-01",
        activity="Create Order",
        timestamp=now,
        attributes={"resource": "User 1"}
    )
    assert event.case_id == "C-01"
    assert event.activity == "Create Order"
    assert event.timestamp == now
    assert event.attributes["resource"] == "User 1"

def test_trace_creation_and_sorting():
    """Tests that a Trace sorts its events by timestamp upon creation."""
    t1 = datetime(2023, 1, 1, 10, 0, 0)
    t2 = datetime(2023, 1, 1, 11, 0, 0)
    
    e1 = Event(case_id="C-01", activity="A", timestamp=t2)
    e2 = Event(case_id="C-01", activity="B", timestamp=t1)
    
    trace = Trace(case_id="C-01", events=[e1, e2])
    
    assert len(trace) == 2
    assert trace.events[0].activity == "B"
    assert trace.events[1].activity == "A"

def test_event_log_creation():
    """Tests the creation of an EventLog object."""
    t1 = Trace(case_id="C-01", events=[])
    t2 = Trace(case_id="C-02", events=[])
    
    log = EventLog(traces=[t1, t2])
    
    assert len(log) == 2
    assert log.get_trace("C-01") == t1
    assert log.get_trace("C-03") is None

def test_event_log_all_events():
    """Tests the `all_events` property of the EventLog."""
    e1 = Event(case_id="C-01", activity="A", timestamp=datetime.now())
    e2 = Event(case_id="C-01", activity="B", timestamp=datetime.now())
    e3 = Event(case_id="C-02", activity="C", timestamp=datetime.now())
    
    t1 = Trace(case_id="C-01", events=[e1, e2])
    t2 = Trace(case_id="C-02", events=[e3])
    
    log = EventLog(traces=[t1, t2])
    
    assert len(log.all_events) == 3