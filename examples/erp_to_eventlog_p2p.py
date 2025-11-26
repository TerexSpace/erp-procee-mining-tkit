"""
Example script demonstrating the transformation of ERP data (procure-to-pay)
into an event log and the discovery of a Directly-Follows Graph.
"""

import pandas as pd
from erp_processminer.io_erp import loaders, mappings
from erp_processminer.discovery import directly_follows
from erp_processminer.visualization import graphs
from erp_processminer.eventlog.serialization import export_log_to_csv

# --- Configuration ---
# This dictionary defines how to map the raw ERP tables to an event log.
MAPPING_CONFIG = {
    "case_id": "PO_NUMBER",
    "tables": {
        "purchase_orders": {
            "entity_id": "PO_NUMBER",
            "activity": "'Create Purchase Order'",
            "timestamp": "CREATION_DATE"
        },
        "goods_receipts": {
            "entity_id": "PO_NUMBER",
            "activity": "'Receive Goods'",
            "timestamp": "RECEIPT_DATE"
        },
        "invoices": {
            "entity_id": "PO_NUMBER",
            "activity": "STATUS", # Activity from a column
            "timestamp": "INVOICE_DATE"
        }
    }
}

def create_sample_data():
    """Creates some in-memory sample data to run the example."""
    po_data = [
        ["PO-001", "2023-01-10", "Vendor A", "User 1"],
        ["PO-002", "2023-01-11", "Vendor B", "User 2"],
    ]
    po_df = pd.DataFrame(po_data, columns=["PO_NUMBER", "CREATION_DATE", "VENDOR", "CREATED_BY"])
    po_df['CREATION_DATE'] = pd.to_datetime(po_df['CREATION_DATE'])

    gr_data = [
        ["GR-101", "PO-001", "2023-01-15", 100, 1],
        ["GR-102", "PO-002", "2023-01-18", 200, 1],
    ]
    gr_df = pd.DataFrame(gr_data, columns=["GR_NUMBER", "PO_NUMBER", "RECEIPT_DATE", "QUANTITY", "ITEM_NUMBER"])
    gr_df['RECEIPT_DATE'] = pd.to_datetime(gr_df['RECEIPT_DATE'])

    inv_data = [
        ["INV-201", "PO-001", "2023-01-20", 1000.0, "Paid"],
        ["INV-202", "PO-002", "2023-01-22", 2000.0, "Paid"],
    ]
    inv_df = pd.DataFrame(inv_data, columns=["INVOICE_NUMBER", "PO_NUMBER", "INVOICE_DATE", "AMOUNT", "STATUS"])
    inv_df['INVOICE_DATE'] = pd.to_datetime(inv_df['INVOICE_DATE'])
    
    return po_df, gr_df, inv_df

def main():
    """Main execution function."""
    print("1. Creating sample ERP data...")
    po_df, gr_df, inv_df = create_sample_data()

    # You can also load from CSV files like this:
    # po_df = loaders.load_erp_data('sample_logs/purchase_orders.csv')
    # gr_df = loaders.load_erp_data('sample_logs/goods_receipts.csv')
    # inv_df = loaders.load_erp_data('sample_logs/invoices.csv')
    
    print("2. Transforming ERP data into an event log...")
    event_log = mappings.apply_mapping([po_df, gr_df, inv_df], MAPPING_CONFIG)
    
    print(f"   -> Successfully created an event log with {len(event_log.traces)} traces.")
    
    # Save the event log to a CSV file for inspection
    export_log_to_csv(event_log, "p2p_event_log.csv")
    print("   -> Event log saved to 'p2p_event_log.csv'")

    print("3. Discovering a Directly-Follows Graph (DFG)...")
    dfg, start_activities, end_activities = directly_follows.discover_dfg(event_log)
    
    print("4. Visualizing the DFG...")
    try:
        graphs.visualize_dfg(
            dfg,
            start_activities,
            end_activities,
            output_file='p2p_dfg' # .png will be added
        )
        print("   -> DFG visualization saved to 'p2p_dfg.png'")
    except Exception as e:
        if "ExecutableNotFound" in str(e):
            print("   -> SKIPPED: Graphviz executable not found. Please install it and add it to your PATH.")
        else:
            print(f"   -> An error occurred during visualization: {e}")

if __name__ == "__main__":
    main()