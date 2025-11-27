import pandas as pd
from erp_processminer.discovery.directly_follows import discover_dfg
from erp_processminer.eventlog.serialization import dataframe_to_log


def test_dfg_counts_frequency_and_start_end():
    data = [
        ["C-01", "A", "2023-01-01T10:00:00"],
        ["C-01", "B", "2023-01-01T11:00:00"],
        ["C-01", "C", "2023-01-01T12:00:00"],
        ["C-02", "A", "2023-01-02T09:00:00"],
        ["C-02", "C", "2023-01-02T10:00:00"],
    ]
    df = pd.DataFrame(data, columns=["case_id", "activity", "timestamp"])
    log = dataframe_to_log(df)

    dfg, start_acts, end_acts = discover_dfg(log)

    assert start_acts == {"A": 2}
    assert end_acts == {"C": 2}
    assert dfg.graph.nodes["A"]["frequency"] == 2
    assert dfg.graph.nodes["B"]["frequency"] == 1
    assert dfg.graph.nodes["C"]["frequency"] == 2

    edges = dfg.get_edges()
    assert edges[("A", "B")]["frequency"] == 1
    assert edges[("B", "C")]["frequency"] == 1
    assert edges[("A", "C")]["frequency"] == 1
