import pandas as pd
import os

excel_path = "c:\\Users\\minky\\Downloads\\sct pjt\\agi tr schedule.xlsx"
output_dir = "c:\\Users\\minky\\Downloads\\sct pjt\\backend\\data"

# Mapping sheet names to output CSV filenames
sheets_to_csv = {
    "Schedule_Data_Option_A": "agi tr schedule.xlsx - Schedule_Data_Option_A.csv",
    "Schedule_Data_Option_B": "agi tr schedule.xlsx - Schedule_Data_Option_B.csv"
}

try:
    xls = pd.ExcelFile(excel_path)
    print(f"Found sheets: {xls.sheet_names}")
    
    for sheet_name, csv_name in sheets_to_csv.items():
        if sheet_name in xls.sheet_names:
            print(f"Processing {sheet_name}...")
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            
            # Ensure Date columns are properly formatted if needed, but simple read/write is usually enough
            output_path = os.path.join(output_dir, csv_name)
            df.to_csv(output_path, index=False)
            print(f"Saved {output_path}")
        else:
            print(f"Warning: Sheet {sheet_name} not found in Excel file.")

except Exception as e:
    print(f"Error processing Excel file: {e}")
