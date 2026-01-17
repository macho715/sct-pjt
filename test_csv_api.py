import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_csv_endpoints():
    print("--- Testing CSV Data Endpoints ---")
    
    # 1. Baseline
    try:
        resp = requests.get(f"{BASE_URL}/api/schedule/baseline")
        print(f"Baseline: {resp.status_code}")
        data = resp.json()
        print(f"Count: {len(data)}")
        if len(data) > 0:
            print("Sample:", data[0])
    except Exception as e:
        print(f"Baseline Failed: {e}")

    # 2. Optimized
    try:
        resp = requests.get(f"{BASE_URL}/api/schedule/optimized")
        print(f"Optimized: {resp.status_code}")
        data = resp.json()
        print(f"Count: {len(data)}")
        if len(data) > 0:
            print("Sample:", data[0])
    except Exception as e:
        print(f"Optimized Failed: {e}")

if __name__ == "__main__":
    test_csv_endpoints()
