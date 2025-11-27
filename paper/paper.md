---
title: 'ERP-ProcessMiner: A toolkit for process mining on ERP event logs'
tags:
  - Python
  - process mining
  - ERP
  - event logs
  - business process management
  - software paper
authors:
  - name: "Expert Software Architect"
    orcid: "0000-0000-0000-0000"
    affiliation: 1
affiliations:
 - name: "Independent"
   index: 1
date: "26 November 2025"
bibliography: reference.lib
---

# Summary

`ERP-ProcessMiner` is a Python toolkit for process mining on relational data from Enterprise Resource Planning (ERP) systems. It provides a workflow to transform ERP tables into event logs and apply core process mining algorithms for discovery, conformance, and performance analysis. It enables researchers and practitioners to easily extract process-centric insights from complex ERP database schemas.

# Statement of Need

Enterprise Resource Planning (ERP) systems are the backbone of many large organizations, storing vast quantities of transactional data. This data is a rich source for process analysis, but it is typically stored in a normalized, relational format that is not directly compatible with traditional process mining tools, which expect a simple, flat event log structure. The task of extracting, correlating, and transforming this data is a significant and often-repeated challenge in both research and practice [@vanderAalst2016]. `ERP-ProcessMiner` directly addresses this challenge by providing a configurable, open-source toolkit to perform this transformation and subsequent analysis within a single, unified Python environment.

# State of the Field

While several mature process mining tools exist, such as ProM, Celonis, and the Python library `pm4py`, they often assume that the data is already in a suitable event log format (e.g., XES). `pm4py` provides powerful and highly optimized algorithms, but the initial data transformation from ERP-specific schemas remains a largely manual task for the user. `ERP-ProcessMiner` complements these tools by focusing specifically on the ERP data-to-event-log pipeline, offering a declarative mapping approach that simplifies this crucial first step.

# Software Description

The `ERP-ProcessMiner` package is organized into several modules, each with a distinct responsibility:

- **`io_erp`**: Handles the loading of ERP data from CSV files and its transformation into an event log based on a user-defined mapping configuration.
- **`eventlog`**: Defines the core data structures for process mining: `Event`, `Trace`, and `EventLog`.
- **`discovery`**: Implements process discovery algorithms, including a Directly-Follows Graph (DFG) miner and a simplified Heuristics Miner.
- **`models`**: Provides data structures for process models, such as `DFG` and `PetriNet`.
- **`conformance`**: Includes algorithms for conformance checking, such as token-based replay.
- **`statistics`**: Offers functions to compute performance metrics (e.g., cycle time) and analyze process variants.
- **`visualization`**: Provides tools to generate visual representations of process models and simple HTML dashboards.

# Illustrative Example

A common use case is analyzing a procure-to-pay (P2P) process from an ERP system. A user might have three separate CSV files: `purchase_orders.csv`, `goods_receipts.csv`, and `invoices.csv`. With `ERP-ProcessMiner`, the user can define a simple JSON configuration that specifies how to link these tables (e.g., using the purchase order number as the case ID) and how to define activities (e.g., from document types or statuses). The toolkit can then automatically generate an event log and discover a DFG, as shown in the quickstart example in the `README.md`.

# Availability and Reuse

`ERP-ProcessMiner` is open-source and distributed under the MIT license. The source code is available on GitHub (https://github.com/TerexSpace/erp-procee-mining-tkit). The package is available on PyPI and can be installed via `pip`. The software is designed to be extensible, with clear stubs for more advanced algorithms and integrations.

# Financial Disclosure

The authors have no financial disclosures to report.

# Acknowledgements

We acknowledge the contributions of the open-source community and the developers of the libraries that `ERP-ProcessMiner` builds upon, including `pandas`, `networkx`, and `graphviz`.

# References