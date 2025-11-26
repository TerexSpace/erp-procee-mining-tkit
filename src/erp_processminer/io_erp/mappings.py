"""
Transforms relational ERP DataFrames into a canonical event log structure
based on a declarative mapping configuration.
"""

from typing import List, Dict, Any
import pandas as pd

from erp_processminer.eventlog.structures import Event, Trace, EventLog

def apply_mapping(
    dataframes: List[pd.DataFrame], 
    config: Dict[str, Any]
) -> EventLog:
    """
    Transforms one or more pandas DataFrames into an EventLog object based on a
    mapping configuration.

    The configuration dictionary specifies how to extract the case ID, activity,
    and timestamp from the tables.

    :param dataframes: A list of pandas DataFrames, each representing an ERP table.
    :param config: A dictionary defining the mapping rules.
    :return: An EventLog object.
    """
    all_events: List[Event] = []
    case_id_col = config['case_id']
    
    # Heuristic to find the right dataframe for each table config
    df_map = {df.columns.name if df.columns.name else f"df_{i}": df for i, df in enumerate(dataframes)}
    
    # A better heuristic would be to inspect columns, but this is a start
    # We assume the user provides dataframes in the same order as the config
    # or that we can distinguish them by some property.
    
    # A simple approach if no names are set on dataframes
    if len(dataframes) == len(config['tables']):
        df_map = {list(config['tables'].keys())[i]: df for i, df in enumerate(dataframes)}


    for table_name, table_config in config['tables'].items():
        if table_name not in df_map:
            raise ValueError(f"No DataFrame found for table '{table_name}' in config.")
        
        df = df_map[table_name]
        
        # Ensure required columns exist
        required_cols = [
            table_config['entity_id'], 
            table_config['timestamp']
        ]
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"DataFrame for '{table_name}' is missing required columns: {required_cols}")

        for _, row in df.iterrows():
            # Activity can be a static string or a column name
            activity_source = table_config['activity']
            if activity_source.startswith("'") and activity_source.endswith("'"):
                activity = activity_source.strip("'")
            else:
                activity = row[activity_source]

            event = Event(
                case_id=str(row[case_id_col]),
                activity=str(activity),
                timestamp=pd.to_datetime(row[table_config['timestamp']]),
                attributes={
                    'source_table': table_name,
                    **{k: v for k, v in row.items() if k not in required_cols}
                }
            )
            all_events.append(event)

    # Group events by case_id and sort them to form traces
    all_events.sort(key=lambda e: (e.case_id, e.timestamp))
    
    traces: Dict[str, Trace] = {}
    for event in all_events:
        if event.case_id not in traces:
            traces[event.case_id] = Trace(case_id=event.case_id, events=[])
        traces[event.case_id].events.append(event)
        
    return EventLog(list(traces.values()))