import pandas as pd
import os

file_path = "c:\\Users\\minky\\Downloads\\sct pjt\\HVDC STATUS (1).xlsx"

try:
    xls = pd.ExcelFile(file_path)
    print(f"Sheet names: {xls.sheet_names}")
    
    for sheet in xls.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet, nrows=5)
        print(f"\n--- Sheet: {sheet} ---")
        print(df.columns.tolist())
        print(df.head())
except Exception as e:
    print(f"Error reading Excel file: {e}")
