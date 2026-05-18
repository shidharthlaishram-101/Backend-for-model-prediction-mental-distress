# Without logger directly from coolterm
import subprocess
import os
import sys

from data_logger import get_user_info
from txt_to_csv_converter import convert_and_clean_txt
from preprocessing import preprocess_data
from feature_extraction import extract_features
from prediction import predict_stress
from firebase_upload import upload_result

def setup_folders():
    folders = [
        'data/raw',
        'data/processed',
        'data/predictions',
        'models',
        'firebase'
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

if __name__ == "__main__":
    setup_folders()
    
    print("STEP 1 - Subject Information")
    get_user_info()
    
    input_file = "data/raw_serial_data.txt"
    if not os.path.exists(input_file):
        print(f"\nError: The file '{input_file}' was not found.")
        print("Please place your raw text file at that location and run the script again.")
        sys.exit(1)
        
    if os.path.getsize(input_file) == 0:
        print(f"\nError: The file '{input_file}' is empty. Please provide a file with data.")
        sys.exit(1)
    
    print("\nSTEP 2 - Convert TXT to CSV")
    convert_and_clean_txt(input_file=input_file, output_file="data/cleaned_output.csv")
    
    print("\nSTEP 3 - Preprocess")
    processed_df = preprocess_data('data/cleaned_output.csv')
    
    if not processed_df.empty:
        print("\nSTEP 4 - Feature Extraction (with Neurokit2)")
        feature_df = extract_features(processed_df)
        
        if not feature_df.empty:
            print("\nSTEP 5 - Prediction (with Scaler)")
            result_df = predict_stress(feature_df)
            
            if not result_df.empty:
                print("Prediction Summary:")
                print(result_df[['Time', 'Stress_Status']].tail())
                
                print("\nSTEP 6 - Upload to Firebase")
                upload_result(result_df)
                print('\nFULL PIPELINE COMPLETED')
            else:
                print("Prediction failed.")
        else:
            print("Feature extraction failed.")
    else:
        print("Preprocessing failed.")
