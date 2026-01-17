import pandas as pd
from .base import BaseSkill

class AntiGravitySkill(BaseSkill):
    @property
    def name(self) -> str:
        return "anti_gravity"

    @property
    def description(self) -> str:
        return "Module to shorten schedule (Crashing) or adjust logic (Recovery) considering Cost Slope when project delay occurs"

    def execute(self, data: pd.DataFrame, params: dict) -> dict:
        """
        Input: 
            data: Activity DataFrame
            params: {'max_budget': float, 'target_days': int}
        """
        budget = params.get('max_budget', 0)
        logs = []
        recovered_days = 0
        
        # QA: Data Validation
        required_cols = ['task_id', 'duration', 'crash_cost', 'is_critical']
        if not all(col in data.columns for col in required_cols):
            return {"status": "error", "msg": f"Missing columns. Required: {required_cols}"}

        df = data.copy()
        
        # --- Core Logic (Simplified) ---
        logs.append(f"Starting Anti-Gravity sequence. Budget: ${budget}")
        
        candidates = df[df['is_critical'] == True].sort_values('crash_cost')
        
        current_cost = 0
        for _, row in candidates.iterrows():
            if current_cost + row['crash_cost'] <= budget:
                # Compress Duration by 1 day
                idx = row.name # original index
                df.at[idx, 'duration'] -= 1
                current_cost += row['crash_cost']
                recovered_days += 1
                logs.append(f"Compressed '{row['task_id']}' by 1 day. Cost: ${row['crash_cost']}")
            else:
                logs.append("Budget limit reached.")
                break
        
        return {
            "status": "success",
            "updated_schedule": df,
            "recovered_days": recovered_days,
            "total_cost": current_cost,
            "logs": logs
        }
