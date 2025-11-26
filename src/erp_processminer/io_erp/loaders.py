"""
Contains functions to load ERP data from external sources like CSV files
into pandas DataFrames.
"""

from pathlib import Path
from typing import List
import pandas as pd

def load_erp_data(file_path: str | Path) -> pd.DataFrame:
    """
    Loads data from a CSV file into a pandas DataFrame.

    :param file_path: The path to the CSV file.
    :return: A pandas DataFrame containing the loaded data.
    """
    if not isinstance(file_path, Path):
        file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"The file was not found at: {file_path}")

    # Convert timestamp columns to datetime objects
    df = pd.read_csv(file_path, parse_dates=True)
    for col in df.columns:
        if 'date' in col.lower() or 'timestamp' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def load_multiple_erp_data(file_paths: List[str | Path]) -> List[pd.DataFrame]:
    """
    Loads data from multiple CSV files into a list of pandas DataFrames.

    :param file_paths: A list of paths to the CSV files.
    :return: A list of pandas DataFrames.
    """
    return [load_erp_data(fp) for fp in file_paths]