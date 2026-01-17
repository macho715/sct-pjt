import pandas as pd
import os

EXCEL_FILE = "agi tr schedule.xlsx"
OUTPUT_DIR = "backend/data"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

try:
    print(f"Reading {EXCEL_FILE}...")
    xl = pd.ExcelFile(EXCEL_FILE)
    
    # 1. Extract Option A
    sheet_a = "Schedule_Data_Option_A"
    if sheet_a in xl.sheet_names:
        print(f"Found {sheet_a}, exporting...")
        df_a = pd.read_excel(xl, sheet_a)
        csv_a = os.path.join(OUTPUT_DIR, "agi tr schedule.xlsx - Schedule_Data_Option_A.csv")
        df_a.to_csv(csv_a, index=False)
        print(f"Saved to {csv_a}")
    else:
        print(f"ERROR: {sheet_a} not found!")

    # 2. Extract Option B
    sheet_b = "Schedule_Data_Option_B"
    if sheet_b in xl.sheet_names:
        print(f"Found {sheet_b}, exporting...")
        df_b = pd.read_excel(xl, sheet_b)
        csv_b = os.path.join(OUTPUT_DIR, "agi tr schedule.xlsx - Schedule_Data_Option_B.csv")
        df_b.to_csv(csv_b, index=False)
        print(f"Saved to {csv_b}")
    else:
        print(f"ERROR: {sheet_b} not found!")

    print("Extraction Complete.")

except Exception as e:
    print(f"Failed to extract: {e}")
