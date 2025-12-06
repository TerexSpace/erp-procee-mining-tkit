# ERP-ProcessMiner Copilot Instructions

## Project Overview
A Python toolkit for transforming relational ERP exports into event logs and applying process mining algorithms (discovery, conformance, performance analysis). Targets researchers, educators, and practitioners bridging ERP schemas with process mining.

## Architecture

### Core Data Flow
```
ERP CSV/Tables → io_erp.loaders → pandas DataFrames → io_erp.mappings → EventLog → discovery/conformance → visualization
```

### Key Module Responsibilities
| Module | Purpose |
|--------|---------|
| `eventlog/structures.py` | Core immutable `Event`, mutable `Trace`, `EventLog` dataclasses |
| `io_erp/mappings.py` | Transforms DataFrames to EventLog via declarative config dict |
| `discovery/directly_follows.py` | Discovers DFG with frequency + avg duration on edges |
| `discovery/heuristics_miner.py` | Builds Petri net from DFG using dependency thresholds |
| `conformance/token_replay.py` | Token-based replay for fitness calculation |
| `models/df_graph.py` | DFG wrapper around `networkx.DiGraph` |
| `models/petri_net.py` | `PetriNet`, `Place`, `Transition`, `Arc`, `Marking` structures |
| `visualization/graphs.py` | Graphviz-based rendering of DFG and Petri nets |

## Mapping Configuration Pattern
The central pattern for ERP→EventLog transformation uses a config dict:
```python
config = {
    "case_id": "PO_NUMBER",  # Column linking all tables
    "tables": {
        "table_name": {
            "entity_id": "PO_NUMBER",
            "activity": "'Static Activity'",  # Quoted = literal, unquoted = column name
            "timestamp": "DATE_COLUMN"
        }
    }
}
event_log = mappings.apply_mapping([df1, df2], config)
```
**Important**: DataFrames must be passed in the same order as `config['tables']` keys.

## Development Commands

```bash
# Install in editable mode with test deps
pip install -e .[tests]

# Run tests
pytest

# Run specific test file
pytest tests/test_eventlog_structures.py

# CLI usage
erp-processminer erp-to-log mapping.json data1.csv data2.csv -o log.csv
erp-processminer discover log.csv --method dfg -o model.png
```

## Code Conventions

### Data Structures
- `Event` is frozen (immutable) dataclass with `case_id`, `activity`, `timestamp`, `attributes`
- `Trace` auto-sorts events by timestamp in `__post_init__`
- All timestamps should be `datetime` objects (use `pd.to_datetime()`)

### Import Style
Use absolute imports within package:
```python
from erp_processminer.eventlog.structures import Event, Trace, EventLog
from erp_processminer.models.petri_net import PetriNet, Place, Transition
```

### Test Pattern
Tests use pytest, no fixtures file—each test creates its own data:
```python
def test_feature():
    e1 = Event(case_id="C-01", activity="A", timestamp=datetime.now())
    trace = Trace(case_id="C-01", events=[e1])
    # assertions...
```

## External Dependencies
- `pandas`, `numpy`: Data handling
- `networkx`: Graph structures (DFG uses `nx.DiGraph`)
- `graphviz`: Visualization (requires system Graphviz binary in PATH)
- Python 3.11+ required

## Key Files for Reference
- `examples/erp_to_eventlog_p2p.py` - Complete workflow example
- `tests/test_eventlog_structures.py` - Test patterns
- `src/erp_processminer/cli.py` - CLI entry point structure
