import pandas as pd
import os

def preprocess_data(input_csv):
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f"Error: {input_csv} not found.")
        return pd.DataFrame()
        
    # Colab expects 'sensor1' as hrv and 'sensor2' as gsr
    if 'sensor1' in df.columns and 'sensor2' in df.columns:
        df = df.rename(columns={"sensor1": "hrv", "sensor2": "gsr"})
    
    # Ensure numeric types
    if 'hrv' in df.columns:
        df['hrv'] = pd.to_numeric(df['hrv'], errors='coerce').ffill().bfill()
    if 'gsr' in df.columns:
        df['gsr'] = pd.to_numeric(df['gsr'], errors='coerce').ffill().bfill()

    output_path = 'data/processed/processed_data.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    return df
