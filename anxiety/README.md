# MindCare: Automated IoT Anxiety Detection Pipeline

An automated machine learning backend pipeline in Python that captures physiological sensor data (such as EDA, HR, etc.) from an ESP32 (or a raw text file), processes it using `scipy`-based feature extraction, predicts anxiety levels via a pre-trained machine learning model, and uploads the results to a Firebase Realtime Database.

## Features

- **Data Logging:** Collects raw sensor data from an ESP32 over a serial connection.
- **Data Cleaning:** Converts raw text data into structured CSV format.
- **Preprocessing:** Handles missing values and filters physiological signals.
- **Feature Extraction:** Utilizes `scipy` to extract meaningful features from raw signals.
- **Anxiety Prediction:** Uses a pre-trained model to predict user anxiety levels.
- **Firebase Integration:** Automatically uploads prediction summaries alongside user metadata to a Firebase Realtime Database.

## Prerequisites

- **Python 3.8+**
- ESP32 hardware properly configured and connected (if using the serial data logger).
- Firebase Realtime Database and service account key.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Backend
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

This project uses `python-dotenv` for managing sensitive credentials and hardware configurations.

1. Create a `.env` file in the root directory (you can copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```
2. Update the `.env` file with your specific configurations:

   ```ini
   FIREBASE_KEY_PATH=firebase/firebase_key.json
   FIREBASE_DATABASE_URL=https://your-firebase-database-url.firebasedatabase.app/
   SERIAL_PORT=COM9
   BAUD_RATE=115200
   ```
3. **Firebase Credentials:** Ensure you place your downloaded Firebase Admin SDK private key at `firebase/firebase_key.json` (or whichever path you configured in the `.env` file).

## Usage

1. **Provide Data:** 
   Place your raw data log (from CoolTerm or the `data_logger.py` script) into `data/raw_serial_data.txt`.
   
2. **Run the Pipeline:**
   ```bash
   python main.py
   ```

3. **Provide Subject Information:** 
   The prompt will ask for your `Name`, `Age`, and `Gender`. This information will be saved to `data/user_info.txt` and attached to the final Firebase upload.

### Running the automated Serial Logger (Optional)

If you want the Python script to directly listen to the ESP32 rather than manually dropping in the `raw_serial_data.txt` file, you can run:

```bash
python data_logger.py
```

This will automatically connect to your configured `SERIAL_PORT` and listen for 10 minutes. Afterwards, you can run `python main.py` to process the newly generated data.

## File Structure

- `main.py`: Entry point for the pipeline.
- `data_logger.py`: Connects to ESP32 over serial and logs raw data.
- `txt_to_csv_converter.py`: Converts raw text data to cleaned CSV.
- `preprocessing.py`: Performs signal preprocessing.
- `feature_extraction.py`: Extracts statistical and physiological features.
- `prediction.py`: Loads the model/scaler and returns anxiety predictions.
- `firebase_upload.py`: Uploads the final results to Firebase.
- `.env`: Environment variables configuration.
- `models/`: Directory where pre-trained `.pkl` models are stored.
- `data/`: Auto-generated folder for temporary data tracking.
