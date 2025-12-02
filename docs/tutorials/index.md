# Tutorials

The following tutorials provide step-by-step guides for common process mining workflows using ERP-ProcessMiner.

## Tutorial 1: From ERP Data to an Event Log (Procure-to-Pay)

This tutorial walks through the process of loading relational ERP data for a procure-to-pay (P2P) process, transforming it into an event log, and discovering a process model.

**Notebook**: [p2p_from_erp_logs.ipynb](p2p_from_erp_logs.ipynb)

**What you'll learn**:
- How to load ERP data from CSV files or create DataFrames
- How to define a declarative mapping configuration
- How to transform relational data into an event log
- How to discover a Directly-Follows Graph (DFG)
- How to visualize the discovered process model

## Tutorial 2: Conformance Checking (Order-to-Cash)

This tutorial demonstrates how to perform conformance checking to compare a process model with an event log for an order-to-cash (O2C) process.

**Notebook**: [o2c_conformance.ipynb](o2c_conformance.ipynb)

**What you'll learn**:
- How to create an event log from tabular data
- How to discover a Petri net using the Heuristics Miner
- How to perform token-based replay for conformance checking
- How to interpret fitness scores and deviation statistics
- How to identify non-conforming traces

## Reproducibility

Both tutorials are designed to produce deterministic outputs when run with the same inputs. Where random processes are involved (e.g., in discovery algorithms), random seeds are fixed to ensure reproducibility.

To run the tutorials:

1. Install ERP-ProcessMiner with development dependencies:
   ```bash
   pip install erp-processminer[tests]
   pip install jupyter
   ```

2. Navigate to the tutorials directory:
   ```bash
   cd docs/tutorials
   ```

3. Start Jupyter:
   ```bash
   jupyter notebook
   ```

4. Open and run the notebook of your choice.
