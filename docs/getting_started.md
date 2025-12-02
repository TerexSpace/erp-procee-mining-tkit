# Getting Started

## Installation

Install ERP-ProcessMiner from PyPI:

```bash
pip install erp-processminer
```

For visualization output, you also need the Graphviz system executable in your `PATH`. See the [Graphviz download page](https://graphviz.org/download/) for OS-specific instructions.

## Quick Example

Here's a minimal example that transforms ERP data into an event log and discovers a process model:

```python
import pandas as pd
from erp_processminer.io_erp import loaders, mappings
from erp_processminer.discovery import directly_follows
from erp_processminer.visualization import graphs

# Load ERP data (or create DataFrames from your source)
po_df = pd.DataFrame({
    "PO_NUMBER": ["PO-001", "PO-002"],
    "CREATION_DATE": pd.to_datetime(["2023-01-10", "2023-01-11"]),
    "VENDOR": ["Vendor A", "Vendor B"]
})

gr_df = pd.DataFrame({
    "PO_NUMBER": ["PO-001", "PO-002"],
    "RECEIPT_DATE": pd.to_datetime(["2023-01-15", "2023-01-18"]),
    "QUANTITY": [100, 200]
})

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

# Transform to event log
event_log = mappings.apply_mapping([po_df, gr_df], config)
print(f"Created event log with {len(event_log.traces)} traces")

# Discover a Directly-Follows Graph
dfg, start_acts, end_acts = directly_follows.discover_dfg(event_log)

# Visualize the DFG (requires Graphviz)
graphs.visualize_dfg(dfg, start_acts, end_acts, output_file='my_dfg')
```

## Command-Line Interface

ERP-ProcessMiner also provides a CLI for common workflows:

```bash
# Transform ERP CSV files into an event log
erp-processminer erp-to-log mapping.json purchase_orders.csv goods_receipts.csv -o log.csv

# Discover a DFG and render it
erp-processminer discover log.csv --method dfg -o dfg.png
```

## Next Steps

- Explore the [Tutorials](tutorials/index) for detailed workflows
- Check the [API Reference](api/index) for module documentation
- See the [examples/](https://github.com/TerexSpace/erp-process-mining-tkit/tree/main/examples) directory for runnable scripts
