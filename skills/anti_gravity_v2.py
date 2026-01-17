import pandas as pd
import numpy as np
from .base import BaseSkill

class AdvancedAntiGravitySkill(BaseSkill):
    @property
    def name(self) -> str:
        return "anti_gravity_hybrid"

    @property
    def description(self) -> str:
        return "Derives optimal schedule reduction scenario by combining Fast-Tracking (process overlap) and Crashing (cost injection)"

    def execute(self, data: pd.DataFrame, params: dict) -> dict:
        """
        params: {
            'target_reduction': int (days),
            'max_budget': float,
            'max_overlap_pct': float (0.1 ~ 0.5),
            'safety_factor': float (1.0 = strict, 0.8 = loose)
        }
        """
        # 1. Init
        df = data.copy()
        
        # Initialize 'applied_lag' if not exists
        if 'applied_lag' not in df.columns:
            df['applied_lag'] = 0
            
        target = params.get('target_reduction', 10)
        budget = params.get('max_budget', 100000)
        max_overlap = params.get('max_overlap_pct', 0.25) # Default 25% overlap allowed
        
        logs = []
        recovered = 0
        spent = 0
        risk_score = 0
        
        # Filter Critical Path only (Assume: is_critical column exists)
        if 'is_critical' not in df.columns:
             return {"status": "error", "msg": "Missing column: is_critical"}
             
        critical_path = df[df['is_critical'] == True].sort_values('task_id')
        
        # ---------------------------------------------------------
        # Phase 1: Fast-Tracking (The "Free" Speed)
        # ---------------------------------------------------------
        logs.append("Phase 1: Attempting Fast-Tracking (Logic Overlap)...")
        
        for idx, row in critical_path.iterrows():
            if recovered >= target: break
            
            # Skip un-overlap-able tasks (Keyword based filtering)
            task_name = str(row.get('task_name', '')).lower()
            if any(x in task_name for x in ['curing', 'test', 'approval']):
                continue
                
            # Calculate potential overlap
            original_dur = row['duration']
            max_lead = int(original_dur * max_overlap)
            
            if max_lead > 0:
                # Apply Negative Lag (Lead) logic simulation
                # In reality this should modify Predecessor relations, but here we simulate via duration effect/lag tracking
                effective_reduction = 1 # Try reducing by 1 day
                
                df.at[idx, 'applied_lag'] = df.at[idx, 'applied_lag'] - effective_reduction # Lag -1
                recovered += effective_reduction
                risk_score += 5 # Risk penalty per day overlapping
                logs.append(f"   -> Overlapped '{row['task_id']}' by {effective_reduction} day (Lead). Risk +5")

        # ---------------------------------------------------------
        # Phase 2: Crashing (The "Bought" Speed)
        # ---------------------------------------------------------
        if recovered < target:
            logs.append(f"Phase 2: Target not met. Engaging Crashing (Budget: ${budget})...")
            
            # Sort by Cost Slope (Cheapest First)
            # Ensure required columns exist
            if 'min_duration' not in df.columns or 'crash_cost_per_day' not in df.columns:
                 logs.append("   Simulation Warning: Missing 'min_duration' or 'crash_cost_per_day'. Crashing skipped.")
            else:
                candidates = df[
                    (df['is_critical'] == True) & 
                    (df['min_duration'] < df['duration'])
                ].sort_values('crash_cost_per_day')
                
                while recovered < target and spent < budget:
                    # Find cheapest option (simple loop re-evaluation)
                    best_option = None
                    
                    # We iterate through candidates again to find available one
                    # Note: Sorting might need re-evaluation if costs change dynamically, but assuming static cost slope here.
                    for idx, row in candidates.iterrows():
                        current_dur = df.at[idx, 'duration']
                        min_dur = df.at[idx, 'min_duration']
                        cost = df.at[idx, 'crash_cost_per_day']
                        
                        if current_dur > min_dur:
                             # Check budget
                             if (spent + cost) <= budget:
                                 best_option = idx
                                 break
                    
                    if best_option is None:
                        logs.append("   No more crashable tasks or budget limit reached.")
                        break
                        
                    cost = df.at[best_option, 'crash_cost_per_day']
                    
                    # Action
                    df.at[best_option, 'duration'] -= 1
                    spent += cost
                    recovered += 1
                    risk_score += 1 # Crashing is less risky than overlapping usually
                    logs.append(f"   -> Crashed '{df.at[best_option, 'task_id']}' by 1 day. Cost: ${cost}")

        # ---------------------------------------------------------
        # Result Summary
        # ---------------------------------------------------------
        status = "Success" if recovered >= target else "Partial Success"
        
        return {
            "status": status,
            "target_days": target,
            "actual_recovered": recovered,
            "cost_incurred": spent,
            "risk_index": risk_score, # Higher is riskier
            "logs": logs,
            "updated_schedule_preview": df[['task_id', 'duration', 'applied_lag']].head().to_dict()
        }
