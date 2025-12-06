# ERP-ProcessMiner: Research Documentation

## Overview

ERP-ProcessMiner is an open-source Python toolkit for transforming relational ERP exports into event logs and applying process mining algorithms. This document provides guidance for researchers who want to use the toolkit in academic studies.

## Citing This Work

If you use ERP-ProcessMiner in your research, please cite:

```bibtex
@software{erp_processminer_2025,
  author       = {Ospanov, Almas and Alonso-Jordá, P. and Zhumadillayeva, Ainur},
  title        = {ERP-ProcessMiner: A toolkit for process mining on ERP event logs},
  year         = {2025},
  publisher    = {GitHub},
  url          = {https://github.com/TerexSpace/erp-process-mining-tkit},
  version      = {0.1.0}
}
```

## Experimental Datasets

We recommend the following publicly available datasets for benchmarking:

| Dataset | Description | Events | DOI |
|---------|-------------|--------|-----|
| **BPI Challenge 2019** | Purchase order handling | 1,595,923 | [10.4121/uuid:d06aff4b-79f0-45e6-8ec8-e19730c248f1](https://doi.org/10.4121/uuid:d06aff4b-79f0-45e6-8ec8-e19730c248f1) |
| **BPI Challenge 2020** | Travel expense claims | 56,437 | [10.4121/uuid:52fb97d4-4588-43c9-9d04-3604d4613b51](https://doi.org/10.4121/uuid:52fb97d4-4588-43c9-9d04-3604d4613b51) |
| **BPI Challenge 2017** | Loan applications | 1,202,267 | [10.4121/uuid:5f3067df-f10b-45da-b98b-86ae4c7a310b](https://doi.org/10.4121/uuid:5f3067df-f10b-45da-b98b-86ae4c7a310b) |
| **Sepsis Cases** | Hospital treatment | 15,214 | [10.4121/uuid:915d2bfb-7e84-49ad-a286-dc35f063a460](https://doi.org/10.4121/uuid:915d2bfb-7e84-49ad-a286-dc35f063a460) |
| **Road Traffic Fines** | Fine management | 561,470 | [10.4121/uuid:270fd440-1057-4fb9-89a9-b699b47990f5](https://doi.org/10.4121/uuid:270fd440-1057-4fb9-89a9-b699b47990f5) |

Download these datasets from [4TU.ResearchData](https://data.4tu.nl/) or the [IEEE Task Force on Process Mining](https://www.tf-pm.org/resources/logs).

## Experimental Setup

### Installation

```bash
pip install erp-processminer

# For development/research with all dependencies
pip install -e .[tests]
```

### Reproducing Experiments

1. **Download datasets** from the sources above
2. **Configure mapping** using JSON configuration files
3. **Run experiments** using the provided scripts

Example experiment script:

```python
import time
from erp_processminer.io_erp import loaders, mappings
from erp_processminer.discovery import directly_follows
from erp_processminer.conformance import token_replay

# Load data
df = loaders.load_erp_data("bpi_2019.csv")

# Configure mapping
config = {
    "case_id": "case:concept:name",
    "tables": {
        "events": {
            "entity_id": "case:concept:name",
            "activity": "concept:name",
            "timestamp": "time:timestamp"
        }
    }
}

# Measure transformation time
start = time.time()
event_log = mappings.apply_mapping([df], config)
transform_time = time.time() - start

# Measure discovery time
start = time.time()
dfg, start_acts, end_acts = directly_follows.discover_dfg(event_log)
discovery_time = time.time() - start

print(f"Traces: {len(event_log)}")
print(f"Events: {len(event_log.all_events)}")
print(f"Transform time: {transform_time:.2f}s")
print(f"Discovery time: {discovery_time:.2f}s")
```

## Methodology Components

### 1. Declarative ERP Mapping

The toolkit's key contribution is a declarative mapping system:

```python
# Static activity (table semantics imply activity)
"activity": "'Create Purchase Order'"

# Dynamic activity (derive from column values)
"activity": "STATUS"
```

### 2. Process Discovery Algorithms

| Algorithm | Output | Complexity | Use Case |
|-----------|--------|------------|----------|
| DFG Discovery | Directed graph | O(n) | Initial exploration |
| Heuristics Miner | Petri net | O(n²) | Noise-tolerant discovery |

### 3. Conformance Checking

Token-based replay computes:

$$fitness = 0.5 \times \left(1 - \frac{missing}{consumed}\right) + 0.5 \times \left(1 - \frac{remaining}{produced}\right)$$

### 4. Performance Metrics

Collect these metrics for benchmarking:

| Metric | Description | Computation |
|--------|-------------|-------------|
| **Fitness** | Log-model alignment | Token replay |
| **Precision** | Model behavior in log | Anti-alignment |
| **F-score** | Harmonic mean | 2×(fitness×precision)/(fitness+precision) |
| **Execution time** | Wall-clock seconds | time.time() |
| **Memory usage** | Peak memory | tracemalloc |

## Comparison with Other Tools

For fair comparison, use identical event logs and measure:

1. **Discovery quality**: Fitness, precision, generalization
2. **Execution time**: Total wall-clock time
3. **Preprocessing effort**: Lines of code, development time

### pm4py Integration

```python
from erp_processminer.integration.pm4py_adapter import to_pm4py_log

# Convert ERP-ProcessMiner log to pm4py format
pm4py_log = to_pm4py_log(event_log)

# Use pm4py algorithms
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
net, im, fm = inductive_miner.apply(pm4py_log)
```

## Experiment Checklist

Before publishing results, verify:

- [ ] All datasets cited with proper DOIs
- [ ] Python version and dependencies documented
- [ ] Hardware specifications noted
- [ ] Random seeds fixed (if applicable)
- [ ] Statistical significance tests performed (for multiple runs)
- [ ] Code and data available in replication package

## Limitations and Scope

**In scope:**
- Declarative ERP-to-event-log transformation
- DFG and Heuristics Miner discovery
- Token-based conformance checking
- Educational/research use cases

**Out of scope:**
- Real-time streaming processing
- Object-centric process mining (OCEL)
- Production-scale (>10M events) processing
- Commercial ERP connectors (SAP, Oracle)

## Future Research Directions

1. **Object-Centric Extension**: Support for OCEL 2.0 format
2. **Streaming Mining**: Incremental model updates
3. **Predictive Monitoring**: LSTM-based next activity prediction
4. **Privacy-Preserving Mining**: Differential privacy for event logs
5. **Automated Mapping**: ML-based schema matching for ERP tables

## Contact

For research collaboration or questions:

- **Repository**: https://github.com/TerexSpace/erp-process-mining-tkit
- **Issues**: https://github.com/TerexSpace/erp-process-mining-tkit/issues

## License

MIT License - Free for research and commercial use. See LICENSE file.
