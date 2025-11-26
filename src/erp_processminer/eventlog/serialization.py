"""
Provides functions for serializing EventLog objects to and from file formats
like CSV.
"""

from pathlib import Path
import pandas as pd

from erp_processminer.eventlog.structures import EventLog, Event, Trace

def log_to_dataframe(log: EventLog) -> pd.DataFrame:
    """
    Converts an EventLog object to a pandas DataFrame.

    :param log: The event log to convert.
    :return: A pandas DataFrame representation of the log.
    """
    records = []
    for trace in log:
        for event in trace:
            # Flatten attributes into the main record
            record = {
                'case_id': event.case_id,
                'activity': event.activity,
                'timestamp': event.timestamp,
                **event.attributes
            }
            records.append(record)
    return pd.DataFrame(records)

def dataframe_to_log(df: pd.DataFrame) -> EventLog:
    """
    Converts a pandas DataFrame into an EventLog object.
    The DataFrame must contain 'case_id', 'activity', and 'timestamp' columns.

    :param df: The DataFrame to convert.
    :return: An EventLog object.
    """
    required_cols = ['case_id', 'activity', 'timestamp']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"DataFrame must contain columns: {required_cols}")

    # Convert to datetime if not already
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    traces_map = {}
    for _, row in df.iterrows():
        case_id = row['case_id']
        
        # Collect other columns as attributes
        attributes = row.drop(required_cols).to_dict()

        event = Event(
            case_id=case_id,
            activity=row['activity'],
            timestamp=row['timestamp'],
            attributes=attributes,
        )

        if case_id not in traces_map:
            traces_map[case_id] = Trace(case_id=case_id, events=[])
        traces_map[case_id].events.append(event)

    # Sort events within each trace
    for trace in traces_map.values():
        trace.events.sort(key=lambda e: e.timestamp)
        
    return EventLog(list(traces_map.values()))

def export_log_to_csv(log: EventLog, file_path: str | Path):
    """
    Exports an event log to a CSV file.

    :param log: The event log to export.
    :param file_path: The path to the output CSV file.
    """
    df = log_to_dataframe(log)
    df.to_csv(file_path, index=False)

def import_log_from_csv(file_path: str | Path) -> EventLog:
    """
    Imports an event log from a CSV file.

    :param file_path: The path to the CSV file.
    :return: An EventLog object.
    """
    df = pd.read_csv(file_path, parse_dates=['timestamp'])
    return dataframe_to_log(df)