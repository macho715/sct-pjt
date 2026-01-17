import sys
import argparse
import csv
from datetime import datetime
import os

# 설정: 템플릿 및 데이터 경로
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(SCRIPT_DIR, '..', 'templates', 'daily_log_fmt.md')
# 프로젝트 루트 기준 data/vessel_schedule.csv
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR))))
SCHEDULE_PATH = os.path.join(PROJECT_ROOT, 'data', 'vessel_schedule.csv')

def get_vessel_info(target_date, vessel_name):
    """
    CSV에서 날짜와 선박명으로 상태를 조회합니다.
    """
    default_info = {"Status": "-", "Location": "-", "Activity": "-"}
    
    try:
        with open(SCHEDULE_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 날짜 형식과 선박명 부분 일치(JPT 71 등) 확인
                if row['Date'] == target_date and vessel_name.lower() in row['Vessel'].lower():
                    return row
    except FileNotFoundError:
        # 경로 문제 시 디버깅용 메시지
        return {"Status": "-", "Location": "-", "Activity": f"File Not Found: {SCHEDULE_PATH}"}
    except Exception as e:
        return {"Status": "-", "Location": "-", "Activity": f"Error: {str(e)}"}
        
    return default_info

def generate_report(site, weather, issue, plan):
    # 1. 오늘 날짜 (데이터 조회용 YYYY-MM-DD)
    today_dt = datetime.now()
    date_key = today_dt.strftime("%Y-%m-%d") # 2026-01-15
    display_date = today_dt.strftime("%Y-%m-%d (%a)")
    
    # 2. 선박 정보 조회 (LCT Bushra, JPT 71)
    # LCT Bushra -> bushra
    # JOPETWIL 71 -> jpt 71 or JPT 71 matched by lower()
    bushra = get_vessel_info(date_key, "bushra")
    jpt71 = get_vessel_info(date_key, "jpt 71")

    # 3. 템플릿 로드
    try:
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            template = f.read()
    except Exception as e:
        return f"Error loading template: {e}"

    # 4. Status Summary 로직
    status_summary = "Normal Operation"
    key_risk = "None"
    
    # 이슈가 있거나 선박이 대기(Standby) 중이면 리스크로 격상
    if issue.lower() != "none":
        status_summary = "Issue Reported"
        key_risk = issue
    elif "waiting" in jpt71.get('Activity', '').lower():
        status_summary = "Vessel Delay"
        key_risk = f"JPT71: {jpt71.get('Activity')}"

    # 5. 데이터 주입
    try:
        report = template.format(
            date=display_date,
            site=site,
            weather=weather,
            issue=issue,
            plan=plan,
            status_summary=status_summary,
            key_risk=key_risk,
            # 선박 데이터 매핑
            bushra_stat=bushra.get('Status', '-'),
            bushra_loc=bushra.get('Location', '-'),
            bushra_rem=bushra.get('Activity', '-'),
            jpt71_stat=jpt71.get('Status', '-'),
            jpt71_loc=jpt71.get('Location', '-'),
            jpt71_rem=jpt71.get('Activity', '-'),
            inbound_qty="Check Manifest"
        )
    except Exception as e:
        return f"Formatting Error: {e}"
    
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', default='DAS')
    parser.add_argument('--weather', default='Sunny')
    parser.add_argument('--issue', default='None')
    parser.add_argument('--plan', default='Routine Work')
    
    args = parser.parse_args()
    print(generate_report(args.site, args.weather, args.issue, args.plan))
