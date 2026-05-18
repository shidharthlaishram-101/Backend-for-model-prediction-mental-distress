# Using logger

# import subprocess
# import os

# from txt_to_csv_converter import convert_and_clean_txt
# from preprocessing import preprocess_data
# from feature_extraction import extract_features
# from prediction import predict_stress
# from firebase_upload import upload_result

# def setup_folders():
#     folders = [
#         'data/raw',
#         'data/processed',
#         'data/predictions',
#         'models',
#         'firebase'
#     ]
#     for folder in folders:
#         os.makedirs(folder, exist_ok=True)

# if __name__ == "__main__":
#     setup_folders()
    
#     print("STEP 1 - Collect Data (CoolTerm Style)")
#     subprocess.run(['python', 'data_logger.py'])
    
#     print("\nSTEP 2 - Convert TXT to CSV")
#     convert_and_clean_txt(input_file="data/raw_serial_data.txt", output_file="data/cleaned_output.csv")
    
#     print("\nSTEP 3 - Preprocess")
#     processed_df = preprocess_data('data/cleaned_output.csv')
    
#     if not processed_df.empty:
#         print("\nSTEP 4 - Feature Extraction (with Neurokit2)")
#         feature_df = extract_features(processed_df)
        
#         if not feature_df.empty:
#             print("\nSTEP 5 - Prediction (with Scaler)")
#             result_df = predict_stress(feature_df)
            
#             if not result_df.empty:
#                 print("Prediction Summary:")
#                 print(result_df[['Time', 'Stress_Status']].tail())
                
#                 print("\nSTEP 6 - Upload to Firebase")
#                 upload_result(result_df)
#                 print('\nFULL PIPELINE COMPLETED')
#             else:
#                 print("Prediction failed.")
#         else:
#             print("Feature extraction failed.")
#     else:
#         print("Preprocessing failed.")
