import requests
import json
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("--- Testing API Connection ---")
    
    # 1. Root
    try:
        resp = requests.get(f"{BASE_URL}/")
        print(f"Root Check: {resp.status_code} - {resp.json()}")
    except Exception as e:
        print(f"Root Check Failed: {e}")
        return

    # 2. Skills List
    resp = requests.get(f"{BASE_URL}/api/skills")
    print(f"Skills List: {resp.status_code}")
    print(resp.json())
    
    # 3. Run Anti-Gravity
    print("\n--- Testing Execution ---")
    mock_data = pd.DataFrame([
        {'task_id': 'A', 'duration': 10, 'crash_cost_per_day': 100, 'is_critical': True, 'min_duration': 8},
        {'task_id': 'B', 'duration': 20, 'crash_cost_per_day': 500, 'is_critical': True, 'min_duration': 15}
    ])
    
    payload = {
        "schedule_json": mock_data.to_json(),
        "target_days": 2,
        "budget": 1000,
        "strategy": "hybrid",
        "max_overlap_pct": 0.25,
        "safety_factor": 1.0
    }
    
    resp = requests.post(f"{BASE_URL}/api/anti-gravity/run", json=payload)
    print(f"Execution: {resp.status_code}")
    print(resp.json())
    
    if resp.status_code == 200:
        print("API Test Passed ✅")
    else:
        print("API Test Failed ❌")

if __name__ == "__main__":
    test_api()
