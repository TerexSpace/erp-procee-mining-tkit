# ERP-ProcessMiner: A toolkit for process mining on ERP event logs

[![PyPI version](https://badge.fury.io/py/erp-processminer.svg)](https://badge.fury.io/py/erp-processminer)
[![Tests](https://github.com/TerexSpace/erp-process-mining-tkit/actions/workflows/tests.yml/badge.svg)](https://github.com/TerexSpace/erp-process-mining-tkit/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/TerexSpace/erp-process-mining-tkit/branch/main/graph/badge.svg)](https://codecov.io/gh/TerexSpace/erp-process-mining-tkit)
[![Documentation Status](https://readthedocs.org/projects/erp-processminer/badge/?version=latest)](https://erp-processminer.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17739836.svg)](https://doi.org/10.5281/zenodo.17739836)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`ERP-ProcessMiner` transforms relational ERP exports into event logs and applies core process mining algorithms for discovery, conformance, and performance analysis. It is designed for researchers, educators, and practitioners who need a lightweight way to bridge ERP schemas with process mining tooling.

## Key Features

- **ERP Data Transformation**: Map relational tables to event logs with flexible definitions for case IDs, activities, and timestamps.
- **Process Discovery**: Discover process models via Directly-Follows Graphs (DFG) and a simplified Heuristics Miner.
- **Conformance Checking**: Token-based replay to quantify deviations between a log and a Petri net.
- **Performance Analysis**: Cycle times, waiting times, and variant statistics for rapid diagnostics.
- **Visualization**: Graphviz-based DFG and Petri net renderings plus a lightweight HTML dashboard.

## Installation

```bash
pip install erp-processminer
# Optional: install Graphviz system binaries for visualization output
```

The Graphviz Python package is installed automatically, but you also need the Graphviz system executable in your `PATH` to render images. See the [Graphviz download page](https://graphviz.org/download/) for OS-specific instructions.

## Usage

### Python API

```python
import pandas as pd
from erp_processminer.io_erp import loaders, mappings
from erp_processminer.discovery import directly_follows
from erp_processminer.visualization import graphs

po_df = loaders.load_erp_data("purchase_orders.csv")
gr_df = loaders.load_erp_data("goods_receipts.csv")

config = {
    "case_id": "PO_NUMBER",
    "tables": {
        "purchase_orders": {"entity_id": "PO_NUMBER", "activity": "'Create PO'", "timestamp": "CREATION_DATE"},
        "goods_receipts": {"entity_id": "PO_NUMBER", "activity": "'Receive Goods'", "timestamp": "RECEIPT_DATE"},
    },
}

event_log = mappings.apply_mapping([po_df, gr_df], config)
dfg, start_acts, end_acts = directly_follows.discover_dfg(event_log)
graphs.visualize_dfg(dfg, start_acts, end_acts, output_file="dfg")
```

### Command-line interface

```bash
# Transform ERP CSV files into an event log
erp-processminer erp-to-log mapping.json purchase_orders.csv goods_receipts.csv -o log.csv

# Discover a DFG and render it
erp-processminer discover log.csv --method dfg -o dfg.png
```

## Testing

Install test dependencies and run the suite:

```bash
pip install -e .[tests]
pytest
```

## Documentation

- Tutorials and guides live in `docs/` (see `docs/index.md` for an entry point).
- A worked example is available in `examples/erp_to_eventlog_p2p.py`.

## Citing

If you use the toolkit in academic work, please see `CITATION.cff` for citation information.

## Community Guidelines

We welcome contributions from the community! Here's how you can get involved:

### Contributing

- **Report bugs**: Open an issue in our [issue tracker](https://github.com/TerexSpace/erp-process-mining-tkit/issues) with a clear description and reproducible example
- **Suggest features**: Propose new features or enhancements through GitHub issues
- **Submit pull requests**: Fork the repository, make your changes, and submit a PR. Please ensure:
  - Your code follows the existing style and conventions
  - Tests are included for new functionality
  - Documentation is updated as needed
  - All tests pass before submission

For detailed contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

### Getting Support

- **Documentation**: Start with the tutorials in `docs/` and example code in `examples/`
- **Issues**: Search existing issues or create a new one for questions and problems
- **Discussions**: Use GitHub Discussions for general questions and community interaction

### Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md) that establishes expected behavior for all community members. We are committed to providing a welcoming and inclusive environment for everyone.

## License

MIT License (see `LICENSE`).
