"""
Tests for the token-based replay conformance checking algorithm.
"""

import pandas as pd
from erp_processminer.eventlog.serialization import dataframe_to_log
from erp_processminer.models.petri_net import PetriNet, Place, Transition, Arc
from erp_processminer.conformance.token_replay import calculate_conformance

def test_token_replay():
    """
    Tests that token-based replay produces a high fitness for a conforming
    trace and a lower fitness for a deviant trace.
    """
    # 1. Create a simple Petri net: start -> A -> p1 -> B -> end
    p_start = Place('start')
    p_end = Place('end')
    p1 = Place('p1')
    t_a = Transition('A', label='A')
    t_b = Transition('B', label='B')
    
    net = PetriNet(
        name='SimpleNet',
        places={p_start, p_end, p1},
        transitions={t_a, t_b},
        arcs={
            Arc(p_start, t_a),
            Arc(t_a, p1),
            Arc(p1, t_b),
            Arc(t_b, p_end)
        }
    )
    net._build_arc_maps()

    # 2. Create a conforming and a deviant event log
    conforming_log_df = pd.DataFrame([
        ['C-01', 'A', '2023-01-01 10:00:00'],
        ['C-01', 'B', '2023-01-01 11:00:00'],
    ], columns=['case_id', 'activity', 'timestamp'])
    conforming_log = dataframe_to_log(conforming_log_df)

    deviant_log_df = pd.DataFrame([
        ['C-02', 'A', '2023-01-02 10:00:00'],
        ['C-02', 'C', '2023-01-02 11:00:00'], # Deviant activity
    ], columns=['case_id', 'activity', 'timestamp'])
    deviant_log = dataframe_to_log(deviant_log_df)

    # 3. Calculate conformance
    conforming_fitness, _ = calculate_conformance(conforming_log, net)
    deviant_fitness, _ = calculate_conformance(deviant_log, net)

    # 4. Assert that conforming fitness is high and deviant is lower
    assert conforming_fitness > 0.99
    assert deviant_fitness < 0.8