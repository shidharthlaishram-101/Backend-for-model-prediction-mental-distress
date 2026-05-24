import pandas as pd
import os

def preprocess_data(input_csv, output_path='data/processed/processed_data.csv'):
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f"Error: {input_csv} not found.")
        return pd.DataFrame()
        
    # Anxiety model uses 'ecg' and 'eda'
    if 'sensor1' in df.columns and 'sensor2' in df.columns:
        df = df.rename(columns={"sensor1": "ecg", "sensor2": "eda"})
    
    # Ensure numeric types
    if 'ecg' in df.columns:
        df['ecg'] = pd.to_numeric(df['ecg'], errors='coerce').ffill().bfill()
    if 'eda' in df.columns:
        df['eda'] = pd.to_numeric(df['eda'], errors='coerce').ffill().bfill()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    return df
