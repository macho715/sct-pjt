from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import pandas as pd
import json
import io
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skills.registry import registry

app = FastAPI()

# CORS Config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for local dev
)

# File Paths
BASE_DIR = os.path.join(os.path.dirname(__file__), "data")
FILE_A = "agi tr schedule.xlsx - Schedule_Data_Option_A.csv"
FILE_B = "agi tr schedule.xlsx - Schedule_Data_Option_B.csv"

def load_csv_as_json(filename):
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        return []
    
    df = pd.read_csv(path)
    # Map columns for Frontend
    df = df.rename(columns={
        'Task': 'name', 
        'Start': 'start', 
        'Duration': 'duration', 
        'Phase': 'phase',
        'ID': 'id'
    })
    
    # Calculate relative start offset
    if not df.empty and 'start' in df.columns:
        df['start_dt'] = pd.to_datetime(df['start'])
        min_date = df['start_dt'].min()
        df['start_offset'] = (df['start_dt'] - min_date).dt.days
    else:
        df['start_offset'] = 0

    return df.fillna("").to_dict(orient="records")

@app.get("/")
def read_root():
    return {"message": "Anti-Gravity API is Online"}

@app.get("/api/skills")
def list_skills():
    return registry.list_skills()

@app.get("/api/schedule/baseline")
def get_baseline():
    return load_csv_as_json(FILE_A)

@app.get("/api/schedule/optimized")
def get_optimized():
    return load_csv_as_json(FILE_B)

@app.get("/api/analysis/compare")
def get_comparison_analysis():
    data_a = load_csv_as_json(FILE_A)
    data_b = load_csv_as_json(FILE_B)
    
    # Group by Phase
    phases = {}
    
    # 1. Aggregate Baseline
    for item in data_a:
        p = item.get('phase', 'Unknown')
        if p not in phases:
            phases[p] = {'baseline': 0.0, 'optimized': 0.0}
        phases[p]['baseline'] += float(item.get('duration', 0))

    # 2. Aggregate Optimized
    for item in data_b:
        p = item.get('phase', 'Unknown')
        if p not in phases:
            phases[p] = {'baseline': 0.0, 'optimized': 0.0}
        phases[p]['optimized'] += float(item.get('duration', 0))
        
    # 3. Format Result
    result = []
    for p, stats in phases.items():
        base = stats['baseline']
        opt = stats['optimized']
        saved = base - opt
        result.append({
            'phase': p,
            'baseline': round(base, 1),
            'optimized': round(opt, 1),
            'saved': round(saved, 1),
            'status': 'Improved' if saved > 0 else ('No Change' if saved == 0 else 'Delayed')
        })
        
    return sorted(result, key=lambda x: x['saved'], reverse=True)

from fastapi import Body
import shutil
from datetime import datetime

@app.post("/api/schedule/save")
def save_schedule(
    option: str = "A", 
    tasks: list = Body(...)
):
    """
    Receives modified tasks from Frontend and saves to CSV.
    """
    filename = FILE_A if option == "A" else FILE_B
    filepath = os.path.join(BASE_DIR, filename)
    
    # 1. Backup original file (Safety First)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    history_dir = os.path.join(BASE_DIR, "history")
    os.makedirs(history_dir, exist_ok=True)
    backup_path = os.path.join(history_dir, f"{filename}.{timestamp}.bak")
    
    if os.path.exists(filepath):
        shutil.copy(filepath, backup_path)
    
    try:
        # 2. Load current CSV to DataFrame
        df = pd.read_csv(filepath)
        
        # 3. Update DataFrame with new dates
        # Convert list of dicts to a quick lookup dictionary
        updates = {t['id']: t for t in tasks}
        
        for index, row in df.iterrows():
            task_id = row.get('ID') or row.get('task_id') # Handle column name variations
            if task_id in updates:
                new_data = updates[task_id]
                # Convert ISO string to YYYY-MM-DD (first 10 chars)
                if 'start' in new_data:
                    df.at[index, 'Start'] = new_data['start'][:10]
                if 'end' in new_data:
                     # CSV might not have 'End', but let's assume it does or we update Duration
                     # Ideally we update Duration too if start/end changes
                     pass # For now, let's stick to user request: update Start/End dates if columns exist

        # 4. Save back to CSV
        df.to_csv(filepath, index=False)
        
        return {"status": "success", "msg": f"Saved version {timestamp}"}
        
    except Exception as e:
        return {"status": "error", "msg": str(e)}

class AnalyzeRequest(BaseModel):
    task_name: str
    duration: float
    notes: str | None = None
    phase: str

def _assess_risk(notes: str, duration: float):
    notes_content = (notes or "").lower()
    risk_level = "Low"
    insight = ""
    
    if "crane" in notes_content or "lifting" in notes_content:
        risk_level = "High"
        insight = "⚠️ **Weather Risk Detected:** Crane/Lifting operations are sensitive to wind. Recommend adding 2 days float."
    elif "permit" in notes_content or "approval" in notes_content:
        risk_level = "Medium"
        insight = "📄 **Admin Delay Risk:** Permit processing may take longer than expected. Verify status."
    elif duration > 20:
        risk_level = "Medium"
        insight = "⏳ **Long Duration Task:** Task > 20 days. Consider splitting into milestones."
    else:
        risk_level = "Low"
        insight = "✅ **Routine Activity:** No specific risks detected."
        
    return risk_level, insight

@app.post("/api/analyze-risk")
def analyze_risk(req: AnalyzeRequest):
    # 1. AI "Thinking" Simulation (1.0s delay)
    time.sleep(1.0)
    
    risk_level, insight = _assess_risk(req.notes, req.duration)

    return {
        "risk_level": risk_level,
        "analysis": insight,
        "recommendation": "Check Resource Availability" if risk_level == "High" else "Monitor Weekly"
    }

@app.get("/api/analysis/bulk-risk")
def bulk_risk_scan():
    # Analyze the OPTIMIZED schedule (Option B)
    data = load_csv_as_json(FILE_B)
    high_risks = []
    
    for task in data:
        # Map CSV fields
        notes = task.get('Notes', "")
        duration = float(task.get('Duration', 0) or 0)
        
        risk_level, insight = _assess_risk(notes, duration)
        
        if risk_level in ["High", "Medium"]:
            high_risks.append({
                "id": task.get('ID'),
                "name": task.get('Task'),
                "phase": task.get('Phase'),
                "risk_level": risk_level,
                "analysis": insight
            })
            
    # Sort: High Risk first
    return sorted(high_risks, key=lambda x: 0 if x['risk_level'] == 'High' else 1)

class OptimizationParams(BaseModel):
    schedule_json: str # JSON string of DataFrame
    target_days: int
    budget: float
    strategy: str = 'hybrid' # 'hybrid' or 'cost_only'
    max_overlap_pct: float = 0.25
    safety_factor: float = 1.0

@app.post("/api/anti-gravity/run")
def run_anti_gravity(params: OptimizationParams):
    try:
        # Convert JSON string back to DataFrame
        data = pd.read_json(io.StringIO(params.schedule_json))
        
        skill_name = 'anti_gravity_hybrid' if params.strategy == 'hybrid' else 'anti_gravity'
        skill = registry.get_skill(skill_name)
        
        if not skill:
            raise HTTPException(status_code=404, detail=f"Skill '{skill_name}' not found")
            
        exec_params = {
            'target_reduction': params.target_days,
            'max_budget': params.budget,
            'max_overlap_pct': params.max_overlap_pct,
            'safety_factor': params.safety_factor
        }
        
        result = skill.execute(data, exec_params)
        
        # Prepare response
        response = {
            "recovered_days": result.get('actual_recovered', result.get('recovered_days', 0)),
            "cost": result.get('cost_incurred', result.get('total_cost', 0)),
            "risk_score": result.get('risk_index', 0),
            "logs": result.get('logs', []),
            "status": result.get('status', 'unknown')
        }
        
        return response
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
