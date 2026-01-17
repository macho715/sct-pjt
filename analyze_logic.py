import pandas as pd
import os

base_dir = "c:\\Users\\minky\\Downloads\\sct pjt\\backend\\data"
file_a = os.path.join(base_dir, "agi tr schedule.xlsx - Schedule_Data_Option_A.csv")
file_b = os.path.join(base_dir, "agi tr schedule.xlsx - Schedule_Data_Option_B.csv")

def analyze_duration(file_path, name):
    try:
        df = pd.read_csv(file_path)
        # Ensure 'Start' and 'End' are datetime
        df['Start'] = pd.to_datetime(df['Start'])
        df['End'] = pd.to_datetime(df['End'])
        
        min_start = df['Start'].min()
        max_end = df['End'].max()
        
        duration = (max_end - min_start).days + 1 # inclusive
        
        print(f"--- {name} ---")
        print(f"Min Start: {min_start}")
        print(f"Max End: {max_end}")
        print(f"Calculated Duration: {duration} days")
        return duration
    except Exception as e:
        print(f"Error analyzing {name}: {e}")
        return 0

dur_a = analyze_duration(file_a, "Option A (Baseline)")
dur_b = analyze_duration(file_b, "Option B (Optimized)")

print(f"\nRecovered Days (Baseline - Optimized): {dur_a - dur_b}")
