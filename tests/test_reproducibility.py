"""
Tests for reproducibility of the ERP-to-event-log transformation.

These tests ensure that given the same ERP input data, the transformation
produces identical event logs, which is critical for reproducible research.
"""

import pandas as pd
from erp_processminer.io_erp.mappings import apply_mapping
from erp_processminer.discovery.directly_follows import discover_dfg
from erp_processminer.eventlog.serialization import dataframe_to_log


def create_test_erp_data():
    """Creates a reproducible set of test ERP data."""
    po_data = [
        ["PO-001", "2023-01-10", "Vendor A", "User 1"],
        ["PO-002", "2023-01-11", "Vendor B", "User 2"],
        ["PO-003", "2023-01-12", "Vendor A", "User 1"],
    ]
    po_df = pd.DataFrame(
        po_data, columns=["PO_NUMBER", "CREATION_DATE", "VENDOR", "CREATED_BY"]
    )
    po_df["CREATION_DATE"] = pd.to_datetime(po_df["CREATION_DATE"])

    gr_data = [
        ["GR-101", "PO-001", "2023-01-15", 100],
        ["GR-102", "PO-002", "2023-01-18", 200],
        ["GR-103", "PO-003", "2023-01-17", 50],
    ]
    gr_df = pd.DataFrame(
        gr_data, columns=["GR_NUMBER", "PO_NUMBER", "RECEIPT_DATE", "QUANTITY"]
    )
    gr_df["RECEIPT_DATE"] = pd.to_datetime(gr_df["RECEIPT_DATE"])

    inv_data = [
        ["INV-201", "PO-001", "2023-01-20", 1000.0, "Paid"],
        ["INV-202", "PO-002", "2023-01-22", 2000.0, "Paid"],
        ["INV-203", "PO-003", "2023-01-25", 500.0, "Paid"],
    ]
    inv_df = pd.DataFrame(
        inv_data, columns=["INVOICE_NUMBER", "PO_NUMBER", "INVOICE_DATE", "AMOUNT", "STATUS"]
    )
    inv_df["INVOICE_DATE"] = pd.to_datetime(inv_df["INVOICE_DATE"])

    return po_df, gr_df, inv_df


def get_test_mapping_config():
    """Returns a reproducible mapping configuration."""
    return {
        "case_id": "PO_NUMBER",
        "tables": {
            "purchase_orders": {
                "entity_id": "PO_NUMBER",
                "activity": "'Create Purchase Order'",
                "timestamp": "CREATION_DATE",
            },
            "goods_receipts": {
                "entity_id": "PO_NUMBER",
                "activity": "'Receive Goods'",
                "timestamp": "RECEIPT_DATE",
            },
            "invoices": {
                "entity_id": "PO_NUMBER",
                "activity": "'Receive Invoice'",
                "timestamp": "INVOICE_DATE",
            },
        },
    }


def test_erp_to_eventlog_reproducibility():
    """
    Tests that the same ERP input produces the same event log on multiple runs.
    
    This is critical for ensuring reproducible research workflows.
    """
    po_df, gr_df, inv_df = create_test_erp_data()
    config = get_test_mapping_config()

    # Run the transformation twice
    log1 = apply_mapping([po_df, gr_df, inv_df], config)
    log2 = apply_mapping([po_df, gr_df, inv_df], config)

    # Verify both runs produce the same number of traces
    assert len(log1.traces) == len(log2.traces)
    assert len(log1.traces) == 3  # One trace per PO

    # Verify traces have the same case IDs
    case_ids_1 = sorted([t.case_id for t in log1.traces])
    case_ids_2 = sorted([t.case_id for t in log2.traces])
    assert case_ids_1 == case_ids_2
    assert case_ids_1 == ["PO-001", "PO-002", "PO-003"]

    # Verify each trace has the same events in the same order
    for case_id in case_ids_1:
        trace1 = log1.get_trace(case_id)
        trace2 = log2.get_trace(case_id)
        
        assert len(trace1.events) == len(trace2.events)
        
        for e1, e2 in zip(trace1.events, trace2.events):
            assert e1.activity == e2.activity
            assert e1.timestamp == e2.timestamp
            assert e1.case_id == e2.case_id


def test_dfg_discovery_reproducibility():
    """
    Tests that DFG discovery produces the same results on multiple runs.
    
    The DFG should have identical node frequencies and edge counts.
    """
    po_df, gr_df, inv_df = create_test_erp_data()
    config = get_test_mapping_config()
    event_log = apply_mapping([po_df, gr_df, inv_df], config)

    # Discover DFG twice
    dfg1, start1, end1 = discover_dfg(event_log)
    dfg2, start2, end2 = discover_dfg(event_log)

    # Verify start and end activities are identical
    assert start1 == start2
    assert end1 == end2

    # Verify all nodes have the same frequencies
    nodes1 = set(dfg1.get_activities())
    nodes2 = set(dfg2.get_activities())
    assert nodes1 == nodes2

    for activity in nodes1:
        assert dfg1.graph.nodes[activity]["frequency"] == dfg2.graph.nodes[activity]["frequency"]

    # Verify all edges have the same frequencies
    edges1 = dfg1.get_edges()
    edges2 = dfg2.get_edges()
    assert set(edges1.keys()) == set(edges2.keys())

    for edge in edges1:
        assert edges1[edge]["frequency"] == edges2[edge]["frequency"]


def test_event_order_determinism():
    """
    Tests that events within a trace are always sorted by timestamp.
    
    This ensures deterministic behavior regardless of input order.
    """
    # Create data where rows are not in chronological order
    log_data = [
        ["C-01", "C", "2023-01-03"],  # Third event
        ["C-01", "A", "2023-01-01"],  # First event
        ["C-01", "B", "2023-01-02"],  # Second event
    ]
    df = pd.DataFrame(log_data, columns=["case_id", "activity", "timestamp"])
    
    # Convert multiple times
    log1 = dataframe_to_log(df)
    log2 = dataframe_to_log(df)
    
    # Verify events are always in chronological order
    trace1 = log1.traces[0]
    trace2 = log2.traces[0]
    
    expected_order = ["A", "B", "C"]
    
    assert [e.activity for e in trace1.events] == expected_order
    assert [e.activity for e in trace2.events] == expected_order
