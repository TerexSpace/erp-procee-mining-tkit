---
title: 'ERP-ProcessMiner: A toolkit for process mining on ERP event logs'
tags:
  - Python
  - process mining
  - ERP
  - event logs
  - business process management
authors:
  - name: Almas Ospanov
    orcid: 0009-0004-3834-130X
    corresponding: true
    affiliation: 1
affiliations:
 - name: Astana IT University, Kazakhstan
   index: 1
   date: 27 November 2025
bibliography: paper.bib
https://github.com/TerexSpace/erp-procee-mining-tkit.git
DOI: https://doi.org/10.5281/zenodo.17739836
---

# Summary

`ERP-ProcessMiner` is a Python toolkit that turns relational exports from Enterprise Resource Planning (ERP) systems into canonical event logs and applies core process mining techniques for discovery, conformance, and performance analysis. The package offers an end-to-end workflow—from declarative mapping of ERP tables, through log construction, to model discovery, evaluation, and visualization—so that researchers and practitioners can extract process-centric insights without leaving the Python ecosystem.

# Statement of Need

ERP systems record the most authoritative view of operational processes, but their data is stored in normalized relational schemas that are not directly compatible with process mining tools. Traditional process mining platforms—including ProM and `pm4py`—assume that data already exists in flat event log formats such as XES or CSV [@vanderAalst2016; @berti2019pm4py]. The manual effort of correlating ERP tables (e.g., linking purchase orders, goods receipts, and invoices via case identifiers), selecting appropriate case identifiers, and deriving meaningful activities from status codes is substantial and often replicated across projects.

`ERP-ProcessMiner` addresses this gap by providing:

1. **Declarative ERP-to-event-log transformation**: A JSON-based configuration system that allows users to specify mappings between relational tables and event logs without writing custom ETL code.
2. **Core process mining algorithms**: Implementation of fundamental discovery algorithms (Directly-Follows Graphs, Heuristics Miner) and conformance checking (token-based replay) specifically optimized for ERP event data.
3. **Educational and research focus**: A lightweight, open-source toolkit particularly aimed at researchers and educators who need repeatable pipelines to prototype, teach, or conduct research on process mining with ERP datasets.

The toolkit has been designed to support research in business process optimization, compliance checking in procurement workflows, and educational programs teaching process mining fundamentals using realistic ERP data scenarios.

# State of the Field

ProM and commercial systems such as Celonis offer mature discovery and conformance algorithms, and `pm4py` provides a rich Python API for those algorithms [@verbeek2010prom; @berti2019pm4py]. However, these tools assume that data is already provided as an event log; they do not include reusable utilities for assembling logs from ERP source tables or for teaching that transformation in educational settings. `ERP-ProcessMiner` complements the existing ecosystem by focusing on the ERP data-to-event-log pipeline, while still exposing familiar constructs (Directly-Follows Graphs, Petri nets, token-based replay) to remain compatible with standard process mining concepts.

# Software Description

The toolkit is organized around explicit stages of the process mining workflow:

- **ERP I/O and mapping** (`io_erp`): Declarative mapping of ERP tables (or CSV exports) into event logs by specifying case IDs, activity derivation rules, and timestamps. The mapper validates required columns and retains auxiliary attributes for later analysis. Functions include `load_erp_data()` for CSV loading and `apply_mapping()` for transformation.
- **Event log structures** (`eventlog`): Immutable `Event`, mutable `Trace`, and `EventLog` containers with serialization helpers for CSV and pandas DataFrames. The `Event` class enforces required attributes (case_id, activity, timestamp) while supporting arbitrary additional attributes.
- **Discovery** (`discovery`): Directly-Follows Graph construction with frequency and duration statistics via `discover_dfg()`, plus a simplified Heuristics Miner (`discover_heuristics_net()`) that synthesizes a Petri net from dependency measures.
- **Models** (`models`): Lightweight representations of Directly-Follows Graphs (`DFGraph`) and Petri nets (`PetriNet`) to keep the package dependency-light, using NetworkX for graph structures.
- **Conformance** (`conformance`): Token-based replay algorithm (`token_replay()`) for log–model fitness evaluation, returning fitness scores and diagnostics for conforming and deviant traces.
- **Statistics and visualization** (`statistics`, `visualization`): Cycle time and variant analysis, Graphviz-based model rendering (`visualize_dfg()`, `visualize_petri_net()`), and HTML dashboard generation for quick inspection.

`ERP-ProcessMiner` is distributed on PyPI, provides a command-line interface (`erp-processminer`) with `erp-to-log` and `discover` subcommands, and includes example notebooks in `docs/tutorials/` and executable scripts in `examples/` to lower the barrier for adoption. All modules include type hints and docstrings for API discoverability.

# Illustrative Example

A common use case is analyzing a procure-to-pay process. Given CSV exports such as `purchase_orders.csv` and `goods_receipts.csv`, the user declares a JSON mapping that identifies `PO_NUMBER` as the case identifier, derives activities from status codes, and specifies timestamp columns:

```python
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
event_log = mappings.apply_mapping([po_df, gr_df], config)
dfg, start_acts, end_acts = directly_follows.discover_dfg(event_log)
```

Running the command-line interface `erp-processminer erp-to-log mapping.json ...` produces a flat event log. The `discover` subcommand can then mine a Directly-Follows Graph or Petri net and render it using Graphviz. A complete worked end-to-end script is provided in `examples/erp_to_eventlog_p2p.py`.

# Availability and Reuse

`ERP-ProcessMiner` is released under the MIT license with source code at https://github.com/TerexSpace/erp-process-mining-tkit. The package is available on PyPI (`erp-processminer`) and installs with `pip`. Continuous integration on GitHub Actions executes the unit test suite across supported Python versions. The repository includes contribution guidelines, a code of conduct, and a citation file to encourage reuse in academic work.

# Quality Control

Quality assurance focuses on reproducibility and correctness of the ERP-to-event-log pipeline and downstream analysis:

- Unit tests cover event log construction, Directly-Follows Graph statistics, conformance replay, and dashboard generation, and run automatically via GitHub Actions on Python 3.11–3.12.
- Examples in `examples/` and notebooks in `docs/tutorials/` demonstrate end-to-end usage on synthetic ERP exports, providing executable smoke tests for the CLI and API.
- The mapping layer validates required columns and timestamps up-front, preventing silent failures when ingesting ERP tables.

# Financial Disclosure

The authors have no financial disclosures to report.

# Acknowledgements

We thank the open-source community and the maintainers of dependencies such as `pandas`, `networkx`, and `graphviz`, which underpin this toolkit.

# References
