import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def generate_synthetic_from_metadata(csv_filepath, num_synthetic_rows=100):
    """
    Reads metadata from a CSV file and generates synthetic time series data
    with a similar structure.

    Args:
        csv_filepath (str): The path to the real CSV file.
        num_synthetic_rows (int): The number of synthetic data points to generate.

    Returns:
        pandas.DataFrame: A DataFrame with synthetic time series data.
    """
    try:
        # Read a few rows of the CSV to infer data types and column names
        df_head = pd.read_csv(csv_filepath, nrows=5)
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_filepath}")
        return None

    column_names = df_head.columns.tolist()
    print(f"Detected columns: {column_names}")
    column_dtypes = df_head.dtypes.to_dict()
    print(f"Detected data types:\n{column_dtypes}")

    timestamp_col = None
    for col in column_names:
        # Heuristic to find a potential timestamp column
        if 'timestamp' in col.lower() or 'date' in col.lower() or 'time' in col.lower():
            timestamp_col = col
            break

    if not timestamp_col:
        print("Warning: Could not automatically identify a timestamp column. Assuming the first column is the timestamp.")
        timestamp_col = column_names[0]

    # Try to infer the frequency of the time series from the real data (optional but helpful)
    try:
        df_for_freq = pd.read_csv(csv_filepath, usecols=[timestamp_col], parse_dates=[timestamp_col], index_col=timestamp_col)
        if len(df_for_freq) > 1:
            inferred_freq = pd.infer_freq(df_for_freq.index)
            print(f"Inferred time series frequency: {inferred_freq}")
        else:
            inferred_freq = 'D' # Default to daily if not enough data
            print("Insufficient data to infer frequency. Defaulting to daily ('D').")
    except Exception as e:
        inferred_freq = 'D' # Default to daily if inference fails
        print(f"Could not infer frequency ({e}). Defaulting to daily ('D').")

    # Generate synthetic dates
    start_date_real = None
    try:
        df_for_start = pd.read_csv(csv_filepath, usecols=[timestamp_col], parse_dates=[timestamp_col])
        if not df_for_start.empty:
            start_date_real = df_for_start[timestamp_col].min()
        else:
            start_date_real = pd.to_datetime('2024-01-01') # Default start if real data is empty
            print("Real data has no timestamps. Defaulting synthetic start date to 2024-01-01.")
    except Exception as e:
        start_date_real = pd.to_datetime('2024-01-01') # Default start if reading fails
        print(f"Could not read start date from real data ({e}). Defaulting synthetic start date to 2024-01-01.")

    synthetic_dates = pd.date_range(start=start_date_real, periods=num_synthetic_rows, freq=inferred_freq)
    synthetic_df = pd.DataFrame(synthetic_dates, columns=[timestamp_col])
    synthetic_df = synthetic_df.set_index(timestamp_col)

    # Generate synthetic data for other columns based on inferred data types
    for col, dtype in column_dtypes.items():
        if col == timestamp_col:
            continue  # Skip the timestamp column

        if pd.api.types.is_numeric_dtype(dtype):
            # Generate random numbers with a similar scale (very basic approach)
            if not df_head[col].dropna().empty:
                mean_val = df_head[col].dropna().mean()
                std_val = df_head[col].dropna().std()
                synthetic_df[col] = np.random.normal(loc=mean_val, scale=std_val, size=num_synthetic_rows)
            else:
                synthetic_df[col] = np.random.randn(num_synthetic_rows) * 10  # Default if no numeric data to learn from

        elif pd.api.types.is_categorical_dtype(dtype) or dtype == 'object':
            # Generate random choices from the unique values in the real data
            unique_vals = df_head[col].dropna().unique()
            if len(unique_vals) > 0:
                synthetic_df[col] = np.random.choice(unique_vals, size=num_synthetic_rows)
            else:
                synthetic_df[col] = [fake.word() for _ in range(num_synthetic_rows)] # Default to random words

        elif pd.api.types.is_datetime64_any_dtype(dtype):
            # Generate synthetic datetimes within a reasonable range
            if start_date_real:
                end_date_synthetic = synthetic_dates[-1] if len(synthetic_dates) > 0 else start_date_real + pd.Timedelta(days=30)
                synthetic_df[col] = pd.to_datetime(np.random.uniform(start_date_real.timestamp(), end_date_synthetic.timestamp(), size=num_synthetic_rows), unit='s')
            else:
                synthetic_df[col] = pd.to_datetime(np.random.randint(pd.Timestamp('2020-01-01').timestamp(), pd.Timestamp('2025-12-31').timestamp(), size=num_synthetic_rows), unit='s')

        else:
            # Default to generating random strings for other data types
            synthetic_df[col] = [fake.word() for _ in range(num_synthetic_rows)]

    return synthetic_df

if __name__ == "__main__":
    real_csv_file = 'Truck_sales.csv'  # Replace with the actual path to your CSV file
    synthetic_data = generate_synthetic_from_metadata(real_csv_file, num_synthetic_rows=150)

    if synthetic_data is not None:
        print("\nGenerated Synthetic Time Series Data:")
        print(synthetic_data.head())