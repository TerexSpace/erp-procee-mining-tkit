"""
Tests for the ERP data loading and mapping functionality.
"""

import pandas as pd
from erp_processminer.io_erp.mappings import apply_mapping

def test_apply_mapping():
    """
    Tests the transformation of mock ERP DataFrames into an EventLog.
    """
    # Create sample DataFrames
    po_data = [["PO-01", "2023-01-01"]]
    po_df = pd.DataFrame(po_data, columns=["PO_NUMBER", "CREATION_DATE"])
    po_df['CREATION_DATE'] = pd.to_datetime(po_df['CREATION_DATE'])

    gr_data = [["GR-101", "PO-01", "2023-01-05"]]
    gr_df = pd.DataFrame(gr_data, columns=["GR_NUMBER", "PO_NUMBER", "RECEIPT_DATE"])
    gr_df['RECEIPT_DATE'] = pd.to_datetime(gr_df['RECEIPT_DATE'])

    # Define the mapping configuration
    config = {
        "case_id": "PO_NUMBER",
        "tables": {
            "purchase_orders": {
                "entity_id": "PO_NUMBER",
                "activity": "'Create PO'",
                "timestamp": "CREATION_DATE"
            },
            "goods_receipts": {
                "entity_id": "PO_NUMBER",
                "activity": "'Receive Goods'",
                "timestamp": "RECEIPT_DATE"
            }
        }
    }

    # Apply the mapping
    log = apply_mapping([po_df, gr_df], config)

    assert len(log.traces) == 1
    trace = log.get_trace("PO-01")
    assert trace is not None
    assert len(trace.events) == 2
    assert trace.events[0].activity == "Create PO"
    assert trace.events[1].activity == "Receive Goods"