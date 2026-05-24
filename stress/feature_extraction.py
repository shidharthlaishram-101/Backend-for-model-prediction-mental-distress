import pandas as pd
import numpy as np
import neurokit2 as nk
from scipy.integrate import trapezoid
import warnings
import os

warnings.filterwarnings('ignore', category=RuntimeWarning, module='neurokit2')

FS = 32
WINDOW_SEC = 120
STEP_SEC = 60

def build_eda_table(df):
    if "gsr" not in df.columns:
        return pd.DataFrame()
        
    eda_signal = df["gsr"].values
    try:
        signals, info = nk.eda_process(eda_signal, sampling_rate=FS)
    except Exception as e:
        print(f"EDA global processing error: {e}")
        return pd.DataFrame()

    WINDOW = FS * WINDOW_SEC
    STEP = FS * STEP_SEC
    rows = []

    for i in range(0, len(eda_signal) - WINDOW, STEP):
        win_phasic = signals["EDA_Phasic"].iloc[i : i + WINDOW].values
        win_tonic = signals["EDA_Tonic"].iloc[i : i + WINDOW].values
        scr_peaks = signals["SCR_Peaks"].iloc[i : i + WINDOW].sum()

        rows.append({
            "Time": i / FS,
            "Label": 0,
            "EDA_SCR_count": scr_peaks,
            "EDA_Phasic_AUC": trapezoid(np.abs(win_phasic)) / FS,
            "EDA_Tonic_Mean": np.mean(win_tonic)
        })
    return pd.DataFrame(rows)

def build_hrv_table(df):
    if "hrv" not in df.columns:
        return pd.DataFrame()
        
    ecg_signal = df["hrv"].values
    cleaned = nk.ecg_clean(ecg_signal, sampling_rate=FS)

    try:
        _, info = nk.ecg_peaks(cleaned, sampling_rate=FS)
        rpeaks = info["ECG_R_Peaks"]
    except Exception as e:
        print(f"Global R-peak detection failed: {e}")
        return pd.DataFrame()

    WINDOW = FS * WINDOW_SEC
    STEP = FS * STEP_SEC
    rows = []

    for start in range(0, len(ecg_signal) - WINDOW, STEP):
        end = start + WINDOW
        win_peaks = rpeaks[(rpeaks >= start) & (rpeaks < end)]

        if len(win_peaks) < 5:
            continue

        try:
            hrv_results = nk.hrv(win_peaks, sampling_rate=FS)
            rows.append({
                "Time": (start + end) / 2 / FS,
                "Label": 0,
                "HRV_RMSSD": hrv_results["HRV_RMSSD"].values[0],
                "HRV_SDNN": hrv_results["HRV_SDNN"].values[0],
                "HRV_MeanNN": hrv_results["HRV_MeanNN"].values[0],
                "HRV_LF": hrv_results.get("HRV_LF", pd.Series([0])).values[0],
                "HRV_HF": hrv_results.get("HRV_HF", pd.Series([0])).values[0],
                "HRV_LFHF": hrv_results.get("HRV_LFHF", pd.Series([0])).values[0],
            })
        except:
            continue
    return pd.DataFrame(rows)

def extract_features(df, output_path='data/processed/features.csv'):
    if df.empty:
        return pd.DataFrame()
        
    eda_df = build_eda_table(df)
    hrv_df = build_hrv_table(df)

    if not eda_df.empty and not hrv_df.empty:
        eda_df["Subject"], hrv_df["Subject"] = "S1", "S1"
        merged_df = pd.merge_asof(
            eda_df.sort_values("Time"),
            hrv_df.sort_values("Time"),
            on="Time",
            by=["Label", "Subject"],
            direction="nearest"
        )
        merged_df['EDA_Tonic_Diff'] = merged_df['EDA_Tonic_Mean'].diff().fillna(0)
        merged_df['HRV_RMSSD_Diff'] = merged_df['HRV_RMSSD'].diff().fillna(0)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        merged_df.to_csv(output_path, index=False)
        return merged_df
    else:
        print("Feature extraction failed: Insufficient data to merge.")
        return pd.DataFrame()
