import pandas as pd
import os

def read_streamflow_data(file_name, folder="data/raw", missing_value_handling="drop", delimiter=","):
    """
    Reads streamflow data from a CSV or TXT file and returns a flow Series indexed by date.

    Assumes:
    - First column = date
    - Second column = flow

    Parameters:
    file_name (str): Name of the streamflow data file.
    folder (str, optional): Folder containing the data file. Default is "data/raw".
    missing_value_handling (str, optional): How to handle missing values.
        - "drop": Remove rows with NaN values.
        - "fill": Fill missing values with the column mean.
    delimiter (str, optional): Delimiter used in the file. Default is "," for CSV.

    Returns:
    pd.Series: Flow data with datetime index.
    """
    file_path = os.path.join(folder, file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Read the file with given delimiter
    df = pd.read_csv(file_path, delimiter=delimiter)

    # Rename first two columns to "date" and "flow"
    if df.shape[1] < 2:
        raise ValueError("Expected at least two columns: [date, flow]")

    df.columns = ["date", "flow"] + list(df.columns[2:])  # ignore extras
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)

    # Handle missing values
    if missing_value_handling == "drop":
        df = df.dropna(subset=["flow"])
    elif missing_value_handling == "fill":
        df["flow"] = df["flow"].fillna(df["flow"].mean())

    return df["flow"]
