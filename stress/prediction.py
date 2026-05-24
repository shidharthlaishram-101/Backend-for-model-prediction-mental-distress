import joblib
import pandas as pd
import numpy as np
import os

MODEL_PATH = 'models/lda_model.pkl'
SCALER_PATH = 'models/subject_scaler.pkl'

FEATURE_COLUMNS = [
    "EDA_SCR_count",
    "EDA_Phasic_AUC",
    "EDA_Tonic_Mean",
    "EDA_Tonic_Diff",
    "HRV_RMSSD",
    "HRV_SDNN",
    "HRV_MeanNN",
    "HRV_LF",
    "HRV_HF",
    "HRV_LFHF",
    "HRV_RMSSD_Diff"
]

def predict_stress(merged_df, output_path='data/predictions/final_predictions.csv'):
    if merged_df.empty:
        return pd.DataFrame()
        
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        print("Error: lda_model.pkl or subject_scaler.pkl not found in models/ folder.")
        return pd.DataFrame()
        
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    X = merged_df[FEATURE_COLUMNS].copy()
    
    if hasattr(scaler, 'feature_names_in_'):
        X = X[scaler.feature_names_in_]

    X_scaled = scaler.transform(X)

    valid_mask = ~np.isnan(X_scaled).any(axis=1)
    X_scaled_clean = X_scaled[valid_mask]
    result_df = merged_df[valid_mask].copy()

    if len(X_scaled_clean) == 0:
        print("No valid rows after scaling for prediction.")
        return pd.DataFrame()

    predictions = model.predict(X_scaled_clean)

    if predictions.ndim > 1 or (predictions.max() <= 1 and predictions.min() >= 0):
        pred_labels = (predictions > 0.5).astype(int)
    else:
        pred_labels = predictions

    result_df["Predicted_Label"] = pred_labels
    
    label_map = {0: 'Non-Stress', 1: 'Stress'}
    result_df['Stress_Status'] = result_df['Predicted_Label'].map(label_map)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    result_df.to_csv(output_path, index=False)
    
    return result_df
