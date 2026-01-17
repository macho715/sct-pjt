import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import os
from .base import BaseSkill

class GanttChartSkill(BaseSkill):
    @property
    def name(self) -> str:
        return "gantt_chart"

    @property
    def description(self) -> str:
        return "Generates a 'Before & After' Gantt Chart comparing the original and optimized schedules."

    def execute(self, data: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Input:
            data: A dictionary containing 'original' and 'updated' DataFrames.
                  OR just a DataFrame (if just visualizing one state).
            params: {
                'output_path': str (optional),
                'title': str (optional)
            }
        """
        # Parse Input
        if isinstance(data, dict):
            df_original = data.get('original')
            df_updated = data.get('updated')
        else:
            df_original = data
            df_updated = None

        title = params.get('title', 'Schedule Comparison')
        output_path = params.get('output_path', 'schedule_comparison.png')

        # Logic to calculate start/end dates (Simple Forward Pass)
        # We assume Critical Path tasks are sequential for visualization if no dependency info is present
        # This is a simplification for visualization purposes
        
        def calculate_dates(df: pd.DataFrame) -> pd.DataFrame:
            df_res = df.copy()
            # If start_day exists, use it. Else calculate relative.
            if 'start_day' not in df_res.columns:
                current_day = 0
                starts = []
                ends = []
                for _, row in df_res.iterrows():
                    starts.append(current_day)
                    dur = row['duration']
                    ends.append(current_day + dur)
                    # Assume simple sequence for critical items or just stack them
                    # If it's critical, we assume it pushes the next task
                    if row.get('is_critical', False):
                        current_day += dur
                        # Apply lag if exists (Simulating lead/lag)
                        applied_lag = row.get('applied_lag', 0)
                        current_day += applied_lag
                df_res['calc_start'] = starts
                df_res['calc_end'] = ends
            else:
                df_res['calc_start'] = df_res['start_day']
                df_res['calc_end'] = df_res['start_day'] + df_res['duration']
            return df_res

        df_orig_proc = calculate_dates(df_original)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot Original (Gray)
        for i, row in df_orig_proc.iterrows():
            ax.barh(
                row['task_id'], 
                row['duration'], 
                left=row['calc_start'], 
                color='lightgray', 
                edgecolor='grey', 
                alpha=0.6,
                label='Original' if i == 0 else ""
            )

        # Plot Updated (Blue/Red)
        if df_updated is not None:
            df_upd_proc = calculate_dates(df_updated)
            for i, row in df_upd_proc.iterrows():
                # Color logic: Red if duration changed, Blue otherwise
                orig_dur = df_orig_proc.loc[df_orig_proc['task_id'] == row['task_id'], 'duration'].values[0] if row['task_id'] in df_orig_proc['task_id'].values else row['duration']
                
                color = 'cornflowerblue'
                if row['duration'] < orig_dur:
                    color = 'salmon' # Crashed
                elif row.get('applied_lag', 0) < 0:
                    color = 'orange' # Fast-Tracked (Lag changed)
                
                ax.barh(
                    row['task_id'], 
                    row['duration'], 
                    left=row['calc_start'], 
                    height=0.4,
                    color=color,
                    edgecolor='black',
                    label='Optimized' if i == 0 else ""
                )
        
        ax.set_xlabel('Days')
        ax.set_ylabel('Activities')
        ax.set_title(title)
        ax.grid(True, axis='x', linestyle='--', alpha=0.5)
        
        # Create custom legend
        gray_patch = mpatches.Patch(color='lightgray', label='Original Schedule')
        blue_patch = mpatches.Patch(color='cornflowerblue', label='Optimized (Unchanged)')
        red_patch = mpatches.Patch(color='salmon', label='Optimized (Crashed)')
        orange_patch = mpatches.Patch(color='orange', label='Optimized (Fast-Tracked)')
        
        ax.legend(handles=[gray_patch, blue_patch, red_patch, orange_patch])
        
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        
        return {
            "status": "success",
            "image_path": os.path.abspath(output_path)
        }
