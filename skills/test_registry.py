import pandas as pd
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skills.registry import registry

def test_registry_lookup():
    print("\n--- Testing Registry Lookup ---")
    skills = registry.list_skills()
    print("Available Skills:", skills)
    
    assert 'anti_gravity' in skills
    assert 'anti_gravity_hybrid' in skills
    print("Registry Lookup: PASS")

def test_anti_gravity_v1():
    print("\n--- Testing Anti-Gravity V1 (Crashing) ---")
    
    # Mock Data
    data = pd.DataFrame({
        'task_id': ['A', 'B', 'C'],
        'duration': [10, 20, 15],
        'crash_cost': [100, 200, 150],
        'is_critical': [True, True, False]
    })
    
    params = {'max_budget': 150}
    skill = registry.get_skill('anti_gravity')
    result = skill.execute(data, params)
    
    print("Logs:", result['logs'])
    print("Recovered:", result['recovered_days'])
    print("Cost:", result['total_cost'])
    
    assert result['recovered_days'] == 1
    assert result['total_cost'] == 100
    print("Anti-Gravity V1: PASS")

def test_anti_gravity_v2():
    print("\n--- Testing Anti-Gravity V2 (Hybrid) ---")
    
    # Mock Data for Hybrid
    # task B is critical and has high duration, potentially overlap-able
    # task C is critical, crashable
    data = pd.DataFrame({
        'task_id': ['A', 'B', 'C'],
        'task_name': ['Foundation', 'Structure Install', 'Finishing'],
        'duration': [10, 20, 15],
        'min_duration': [8, 15, 12],
        'crash_cost_per_day': [500, 1000, 100], # C is cheap to crash
        'is_critical': [True, True, True],
        'applied_lag': [0, 0, 0]
    })
    
    # Strategy: 
    # Target 3 days.
    # Phase 1: Overlap B (20 * 0.25 = 5 days max). 
    # Let's say we overlap B by 1 day.
    # Phase 2: Crash. C is cheapest (100).
    
    params = {
        'target_reduction': 2,
        'max_budget': 200,
        'max_overlap_pct': 0.1
    }
    
    skill = registry.get_skill('anti_gravity_hybrid')
    result = skill.execute(data, params)
    
    print("Logs:", result['logs'])
    print("Recovered:", result['actual_recovered'])
    print("Risk Index:", result['risk_index'])
    
    assert result['actual_recovered'] >= 1
    print("Anti-Gravity V2: PASS")

if __name__ == "__main__":
    test_registry_lookup()
    test_anti_gravity_v1()
    test_anti_gravity_v2()
