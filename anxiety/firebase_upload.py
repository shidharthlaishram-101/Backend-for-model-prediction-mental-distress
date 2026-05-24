import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv

load_dotenv()

FIREBASE_KEY_PATH = os.getenv('FIREBASE_KEY_PATH', 'firebase/firebase_key.json')
DATABASE_URL = os.getenv('FIREBASE_DATABASE_URL', '')

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(FIREBASE_KEY_PATH)
        firebase_admin.initialize_app(cred, {
            'databaseURL': DATABASE_URL
        })
    except Exception as e:
        print(f"Warning: Firebase initialization failed. Please ensure '{FIREBASE_KEY_PATH}' exists.\nError: {e}")

def fetch_user_id():
    try:
        # Fetching from a generic 'current_user_id' node. Adjust path if necessary.
        ref = db.reference('current_user_id')
        return ref.get()
    except Exception as e:
        print(f"Failed to fetch user ID: {e}")
        return None

def get_user_name():
    try:
        with open('data/user_info.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("Name:"):
                    return line.split("Name:")[1].strip()
    except Exception:
        pass
    return "Unknown User"

def upload_result(result_df):
    if result_df.empty:
        print("No predictions to upload.")
        return
        
    try:
        # We upload the most recent window result to match the Colab logic
        latest_data = result_df.iloc[-1].to_dict()
        
        filtered_data = {
            'Time': latest_data.get('Time'),
            'Anxiety_Status': latest_data.get('Anxiety_Status'),
            'Predicted_Label': latest_data.get('Predicted_Label'),
            'User_Name': get_user_name()
        }
        
        ref = db.reference('anxiety_monitoring/latest')
        ref.set(filtered_data)
        print(f'Successfully uploaded latest prediction for {filtered_data["User_Name"]} to Firebase!')
    except Exception as e:
        print(f"Failed to upload to Firebase: {e}")
