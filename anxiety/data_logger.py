import serial
import time
import os
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv('SERIAL_PORT', 'COM9')

# IMPORTANT:
# Must match ESP32 Serial.begin(...)
BAUD_RATE = int(os.getenv('BAUD_RATE', 115200))

DURATION = 600  # 10 minutes

# Raw chunk size
CHUNK_SIZE = 4096


# ---------------- USER INFO ----------------
def get_user_info():

    print("\n--- Subject Information ---")

    name = input("Enter User Name: ")
    age = input("Enter Age: ")
    gender = input("Enter Gender: ")

    print("---------------------------\n")

    os.makedirs('data', exist_ok=True)

    user_info_path = 'data/user_info.txt'

    with open(user_info_path, 'w', encoding='utf-8') as f:

        f.write(f"Name: {name}\n")
        f.write(f"Age: {age}\n")
        f.write(f"Gender: {gender}\n")

    print(f"User information saved to {user_info_path}!")


# ---------------- MAIN ----------------
def main():

    # Create data folder
    os.makedirs('data', exist_ok=True)

    # Ask subject info
    get_user_info()

    # Output file
    output_filename = 'data/raw_serial_data.txt'

    try:

        ser = serial.Serial(
            PORT,
            BAUD_RATE,
            timeout=0.01
        )

        print(f"\nConnected to {PORT} at {BAUD_RATE} baud.")

    except Exception as e:

        print(f"Error connecting to serial port: {e}")
        return

    # Wait for ESP32 auto-reset
    time.sleep(2)

    # Clear startup buffer
    ser.reset_input_buffer()

    start = time.time()

    total_bytes = 0

    print(
        f"\nCollecting RAW serial data for "
        f"{DURATION} seconds..."
    )

    print(f"Saving to: {output_filename}\n")

    # Open in binary mode
    with open(output_filename, 'wb',
              buffering=1024 * 1024) as f:

        while time.time() - start < DURATION:

            try:

                waiting = ser.in_waiting

                if waiting:

                    # Read raw bytes directly
                    data = ser.read(
                        min(waiting, CHUNK_SIZE)
                    )

                    # Save EXACT raw data
                    f.write(data)

                    total_bytes += len(data)

                else:
                    time.sleep(0.001)

            except Exception as e:

                print("Read Error:", e)

    ser.close()

    print("\n===== COLLECTION FINISHED =====")

    print(f"Total bytes saved : {total_bytes}")

    print(f"Saved file        : {output_filename}")


# ---------------- RUN ----------------
if __name__ == "__main__":
    main()