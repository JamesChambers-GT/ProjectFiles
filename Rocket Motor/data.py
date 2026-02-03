import serial
import pandas as pd
import time
import os

PORT = 'COM3'
BAUD = 57600

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

data = []
header = None

print("\nRunning...\n")

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            continue

        parts = line.split(',')

        if not header and not parts[0].replace('.', '').isdigit():
            header = parts
            continue

        try:
            values = [float(x) for x in parts]
            data.append(values)
        except ValueError:
            continue

except KeyboardInterrupt:
    print("Stopping acquisition...")

if not header:
    header = ['timestamp_ms', 'loadcell1', 'loadcell2', 'total']

df = pd.DataFrame(data, columns=header)

# 🔑 GUARANTEED same-folder save
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, 'loadcell_data.xlsx')

df.to_excel(OUTPUT_PATH, index=False)
print(f"Saved file to: {OUTPUT_PATH}")
