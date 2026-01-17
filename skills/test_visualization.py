import pandas as pd
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skills.registry import registry

def test_gantt_chart():
    print("\n--- Testing Gantt Chart Visualization ---")
    
    # Mock Data: Original
    df_original = pd.DataFrame({
        'task_id': ['Task A', 'Task B', 'Task C', 'Task D'],
        'duration': [10, 20, 15, 12],
        'is_critical': [True, True, True, False],
        'applied_lag': [0, 0, 0, 0],
        'start_day': [0, 10, 30, 0] # Explicit start days for better viz
    })
    
    # Mock Data: Optimized
    # Task A: Unchanged
    # Task B: Overlapped (Lag -2), Duration same (20) -> Start shifts to 8
    # Task C: Crashed (Duration 12) -> Start shifts to 8+20 = 28
    # Task D: Unchanged
    df_updated = pd.DataFrame({
        'task_id': ['Task A', 'Task B', 'Task C', 'Task D'],
        'duration': [10, 20, 12, 12], # C crashed
        'is_critical': [True, True, True, False],
        'applied_lag': [0, -2, 0, 0], # B overlapped
        'start_day': [0, 8, 28, 0] # Recalculated starts
    })
    
    skill = registry.get_skill('gantt_chart')
    params = {
        'title': 'Test Schedule Optimization',
        'output_path': 'skills/test_chart.png'
    }
    
    result = skill.execute({'original': df_original, 'updated': df_updated}, params)
    
    print("Result:", result)
    
    assert result['status'] == 'success'
    assert os.path.exists(result['image_path'])
    print(f"Gantt Chart generated at: {result['image_path']}")

if __name__ == "__main__":
    test_gantt_chart()
