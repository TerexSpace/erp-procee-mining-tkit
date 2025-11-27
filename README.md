# ERP-ProcessMiner: A toolkit for process mining on ERP event logs

[![JOSS status](https://joss.theoj.org/papers/10.21105/joss.01234/status.svg)](https://joss.theoj.org/papers/10.21105/joss.01234)
[![PyPI version](https://badge.fury.io/py/erp-processminer.svg)](https://badge.fury.io/py/erp-processminer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`ERP-ProcessMiner` is a Python toolkit for process mining on relational data from Enterprise Resource Planning (ERP) systems. It provides a workflow to transform ERP tables into event logs and apply core process mining algorithms for discovery, conformance, and performance analysis. It enables researchers and practitioners to easily extract process-centric insights from complex ERP database schemas.

## JOSS Paper

For a detailed academic overview, please see our paper published in the Journal of Open Source Software (JOSS).

## Key Features

- **ERP Data Transformation**: Load relational tables and map them to event logs with flexible definitions for case ID, activity, and timestamp.
- **Process Discovery**: Discover process models from event logs using algorithms like Directly-Follows Graphs and a Heuristics Miner.
- **Conformance Checking**: Analyze deviations between a process model and an event log using token-based replay.
- **Performance Analysis**: Compute key performance indicators such as cycle times, waiting times, and identify process variants.
- **Visualization**: Generate graphical representations of process models and performance dashboards.

## Installation

You can install `erp-processminer` via pip:

```bash
pip install erp-processminer
```

**Note on Graphviz**: To use the visualization features, you must also install the Graphviz software. Please see the [Graphviz download page](https://graphviz.org/download/) for instructions for your operating system. Make sure to add Graphviz to your system's PATH.

## Quickstart Example

This example demonstrates how to load ERP-style data (from CSV files), transform it into an event log, and discover a Directly-Follows Graph (DFG).

Assume you have two CSV files: `purchase_orders.csv` and `goods_receipts.csv`.

**1. Load ERP Data**

```python
import pandas as pd
from erp_processminer.io_erp import loaders, mappings
from erp_processminer.discovery import directly_follows
from erp_processminer.visualization import graphs

# Load raw data from CSV files into pandas DataFrames
po_df = loaders.load_erp_data('purchase_orders.csv')
gr_df = loaders.load_erp_data('goods_receipts.csv')

# Define a mapping configuration
# This tells the tool how to create an event log from the tables.
config = {
    'case_id': 'PO_NUMBER',
    'tables': {
        'purchase_orders': {
            'entity_id': 'PO_NUMBER',
            'activity': "'Create Purchase Order'", # Static activity name
            'timestamp': 'CREATION_DATE'
        },
        'goods_receipts': {
            'entity_id': 'PO_NUMBER',
            'activity': "'Receive Goods'",
            'timestamp': 'RECEIPT_DATE'
        }
    }
}

# 2. Transform to Event Log
event_log = mappings.apply_mapping([po_df, gr_df], config)

print(f"Successfully created an event log with {len(event_log)} traces and {sum(len(t) for t in event_log)} events.")

# 3. Discover a Directly-Follows Graph
dfg, start_activities, end_activities = directly_follows.discover_dfg(event_log)

# 4. Visualize the DFG
# This will generate a file named 'dfg.png'
graphs.visualize_dfg(dfg, start_activities, end_activities, output_file='dfg.png')

print("Discovered and visualized the Directly-Follows Graph at 'dfg.png'.")
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.