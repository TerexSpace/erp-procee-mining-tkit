"""
Tests for the simplified Heuristics Miner algorithm.
"""

import pandas as pd
from erp_processminer.eventlog.serialization import dataframe_to_log
from erp_processminer.discovery.heuristics_miner import discover_petri_net_with_heuristics

def test_heuristics_miner():
    """
    Tests that the heuristics miner discovers a plausible Petri net from a
    simple log.
    """
    # Create a simple event log
    log_data = [
        ['C-01', 'A', '2023-01-01 10:00:00'],
        ['C-01', 'B', '2023-01-01 11:00:00'],
        ['C-01', 'C', '2023-01-01 12:00:00'],
        ['C-02', 'A', '2023-01-02 10:00:00'],
        ['C-02', 'B', '2023-01-02 11:00:00'],
        ['C-02', 'C', '2023-01-02 12:00:00'],
    ]
    log_df = pd.DataFrame(log_data, columns=['case_id', 'activity', 'timestamp'])
    log = dataframe_to_log(log_df)

    # Discover the Petri net
    net = discover_petri_net_with_heuristics(log, dependency_thresh=0.1)

    # Assert basic properties of the discovered net
    assert len(net.places) == 4 # start, end, p_(A,B), p_(B,C)
    assert len(net.transitions) == 3 # A, B, C
    
    activity_names = {t.label for t in net.transitions}
    assert activity_names == {'A', 'B', 'C'}
    
    # Check for expected arcs
    start_place = [p for p in net.places if p.name == 'start'][0]
    a_trans = [t for t in net.transitions if t.label == 'A'][0]
    
    assert any(arc.source == start_place and arc.target == a_trans for arc in net.arcs)