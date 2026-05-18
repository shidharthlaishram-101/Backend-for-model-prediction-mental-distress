import pandas as pd
import os

def convert_and_clean_txt(input_file="data/raw_serial_data.txt", output_file="data/cleaned_output.csv"):
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' was not found.")
        return

    print(f"Reading data from {input_file}...")
    # Read the text file (assumes comma-separated without a header)
    df = pd.read_csv(input_file, header=None)

    # Add column names based on your specification
    df.columns = ["timestamp", "sensor1", "sensor2", "status"]

    print("Cleaning data...")
    # Replace invalid values (-1 and "NA") with NaN
    df.replace([-1, "NA"], pd.NA, inplace=True)

    # Forward fill (use previous row value to fill missing gaps)
    df.ffill(inplace=True)

    # Optional: if first rows are still NaN -> backfill
    df.bfill(inplace=True)

    # Save cleaned data
    df.to_csv(output_file, index=False)
    print(f"Conversion successful! Cleaned CSV saved as: {output_file}")

if __name__ == "__main__":
    convert_and_clean_txt()
