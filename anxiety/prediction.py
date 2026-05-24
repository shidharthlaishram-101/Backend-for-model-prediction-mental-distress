import joblib
import pandas as pd
import numpy as np
import os

MODEL_PATH = 'models/best_model_RandomForest.pkl'

FEATURE_COLUMNS = [
    "ecg_mean", "ecg_std", "ecg_min", "ecg_max", "ecg_rms",
    "ecg_hrv_std", "ecg_hrv_mean",
    "eda_mean", "eda_std", "eda_min", "eda_max", "eda_slope", "eda_npeaks"
]

def predict_anxiety(merged_df, output_path='data/predictions/final_predictions.csv'):
    if merged_df.empty:
        return pd.DataFrame()
        
    if not os.path.exists(MODEL_PATH):
        print(f"Error: {MODEL_PATH} not found.")
        return pd.DataFrame()
        
    model = joblib.load(MODEL_PATH)

    X = merged_df[FEATURE_COLUMNS].copy()
    
    valid_mask = ~np.isnan(X).any(axis=1)
    X_clean = X[valid_mask]
    result_df = merged_df[valid_mask].copy()

    if len(X_clean) == 0:
        print("No valid rows after filtering NaNs for prediction.")
        return pd.DataFrame()

    # Pass .values to bypass "feature names do not match" warnings from sklearn SMOTE
    predictions = model.predict(X_clean.values)

    result_df["Predicted_Label"] = predictions
    
    # 0 = Baseline, 1 = Anxiety
    label_map = {0: 'Baseline', 1: 'Anxiety'}
    result_df['Anxiety_Status'] = result_df['Predicted_Label'].map(label_map)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    result_df.to_csv(output_path, index=False)
    
    return result_df
