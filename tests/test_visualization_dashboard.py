from pathlib import Path

from erp_processminer.eventlog.structures import EventLog
from erp_processminer.visualization.dashboards import generate_dashboard


def test_generate_dashboard_handles_empty_log(tmp_path: Path):
    log = EventLog(traces=[])
    output = tmp_path / "dashboard.html"

    generate_dashboard(log, output_file=str(output))

    assert output.exists()
    assert output.stat().st_size > 0
