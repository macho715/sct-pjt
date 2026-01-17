#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HVDC STATUS Excel → shipping_list.csv 변환기
==============================================
- HVDC STATUS (1).xlsx 파일을 Logi-Tracker용 CSV로 변환
- Flow Code v3.5 자동 계산
- AGI/DAS 규칙 적용 (MOSB 경유 필수)
"""

import os
import sys
import csv
from datetime import datetime

# pandas 사용 (Excel 읽기)
try:
    import pandas as pd
except ImportError:
    print('{"error": true, "message": "pandas 라이브러리가 필요합니다. pip install pandas openpyxl"}')
    sys.exit(1)

# 경로 설정
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
EXCEL_PATH = os.path.join(PROJECT_ROOT, 'HVDC STATUS (1).xlsx')
OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'data', 'shipping_list.csv')

# 오늘 날짜 (2026-01-15 기준)
TODAY = datetime(2026, 1, 15)

# 컬럼 매핑
COLUMN_MAP = {
    'source': {
        'NO': 'NO',
        'SCT SHIP NO.': 'SCT_Ship_No',
        'PO No.': 'PO_No',
        'VENDOR': 'Vendor',
        'MAIN DESCRIPTION (PO)': 'Item',
        'POL': 'From',
        'POD': 'To',
        'B/L No./\n AWB No.': 'AWB_No',
        'SHIP\n MODE': 'Ship_Mode',
        'ETA': 'ETA',
        'ATA': 'ATA',
        'ETD': 'ETD',
        'ATD': 'ATD',
        'MOSB': 'MOSB_Date',
        'AAA Storage': 'WH_Date',
        'SHU': 'SHU',
        'DAS': 'DAS',
        'MIR': 'MIR',
        'AGI': 'AGI',
        'DELIVERY DATE': 'Delivery_Date',
        'Customs\n Start': 'Customs_Start',
        'Customs\n Close': 'Customs_Close',
        'GWT\n (KG)': 'Weight_KG',
        'CBM': 'CBM',
    }
}


def determine_final_site(row):
    """목적지 사이트 결정 (SHU/DAS/MIR/AGI)"""
    sites = []
    if pd.notna(row.get('SHU')) and row.get('SHU') not in ['', 0, '0']:
        sites.append('SHU')
    if pd.notna(row.get('DAS')) and row.get('DAS') not in ['', 0, '0']:
        sites.append('DAS')
    if pd.notna(row.get('MIR')) and row.get('MIR') not in ['', 0, '0']:
        sites.append('MIR')
    if pd.notna(row.get('AGI')) and row.get('AGI') not in ['', 0, '0']:
        sites.append('AGI')
    
    if len(sites) == 1:
        return sites[0]
    elif len(sites) > 1:
        return '/'.join(sites)
    return 'Unknown'


def calculate_flow_code(row):
    """
    Flow Code v3.5 자동 계산
    
    Flow 0: Pre Arrival (통관 대기)
    Flow 1: Port → Site (직접 배송)
    Flow 2: Port → WH → Site (창고 경유)
    Flow 3: Port → MOSB → Site (MOSB 경유)
    Flow 4: Port → WH → MOSB → Site (전체 체인)
    Flow 5: Mixed/Incomplete (비정상)
    """
    has_customs = pd.notna(row.get('Customs_Close'))
    has_warehouse = pd.notna(row.get('WH_Date'))
    has_mosb = pd.notna(row.get('MOSB_Date'))
    has_delivery = pd.notna(row.get('Delivery_Date'))
    final_site = row.get('Final_Site', 'Unknown')
    
    # AGI/DAS 목적지는 반드시 MOSB 경유 필요
    requires_mosb = final_site in ['AGI', 'DAS', 'AGI/DAS', 'DAS/AGI']
    
    # Flow Code 결정
    if not has_customs:
        flow_code = 0  # Pre Arrival
        flow_desc = "Pre Arrival (통관 대기)"
    elif has_warehouse and has_mosb:
        flow_code = 4  # Port → WH → MOSB → Site
        flow_desc = "Port → WH → MOSB → Site"
    elif has_mosb:
        flow_code = 3  # Port → MOSB → Site
        flow_desc = "Port → MOSB → Site"
    elif has_warehouse:
        flow_code = 2  # Port → WH → Site
        flow_desc = "Port → WH → Site"
    elif has_delivery:
        flow_code = 1  # Port → Site (직접)
        flow_desc = "Port → Site (직접)"
    else:
        flow_code = 5  # Incomplete
        flow_desc = "Mixed/Incomplete"
    
    # AGI/DAS 규칙 검사: Flow < 3인데 MOSB 필요 → 규칙 위반
    compliance = "PASS"
    if requires_mosb and flow_code < 3 and flow_code != 0:
        compliance = "FAIL: MOSB 경유 필수"
    
    return flow_code, flow_desc, compliance


def determine_status(row):
    """화물 상태 결정"""
    has_delivery = pd.notna(row.get('Delivery_Date'))
    has_eta = pd.notna(row.get('ETA'))
    has_customs_close = pd.notna(row.get('Customs_Close'))
    has_mosb = pd.notna(row.get('MOSB_Date'))
    
    if has_delivery:
        return 'Arrived'
    elif has_mosb:
        return 'At MOSB'
    elif has_customs_close:
        return 'Customs Cleared'
    elif has_eta:
        return 'In-Transit'
    else:
        return 'Pending'


def format_date(value):
    """날짜 포맷팅"""
    if pd.isna(value):
        return ''
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d')
    if isinstance(value, str):
        return value[:10] if len(value) >= 10 else value
    return str(value)


def convert_hvdc_to_csv():
    """HVDC STATUS Excel → CSV 변환 실행"""
    print(f"📂 Excel 파일 읽는 중: {EXCEL_PATH}")
    
    try:
        df = pd.read_excel(EXCEL_PATH)
    except FileNotFoundError:
        return {"error": True, "message": f"파일을 찾을 수 없습니다: {EXCEL_PATH}"}
    except Exception as e:
        return {"error": True, "message": f"Excel 읽기 실패: {str(e)}"}
    
    print(f"✅ {len(df)}개 레코드 로드됨")
    
    # 출력 디렉토리 생성
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    # 변환된 데이터 저장
    converted_rows = []
    
    for idx, row in df.iterrows():
        # 기본 필드 추출
        converted = {
            'NO': row.get('NO', ''),
            'SCT_Ship_No': row.get('SCT SHIP NO.', ''),
            'PO_No': row.get('PO No.', ''),
            'AWB_No': row.get('B/L No./\n AWB No.', ''),
            'Vendor': row.get('VENDOR', ''),
            'Item': row.get('MAIN DESCRIPTION (PO)', ''),
            'From': row.get('POL', ''),
            'To': row.get('POD', ''),
            'Ship_Mode': row.get('SHIP\n MODE', ''),
            'ETA': format_date(row.get('ETA')),
            'ATA': format_date(row.get('ATA')),
            'Customs_Start': format_date(row.get('Customs\n Start')),
            'Customs_Close': format_date(row.get('Customs\n Close')),
            'WH_Date': format_date(row.get('AAA Storage')),
            'MOSB_Date': format_date(row.get('MOSB')),
            'Delivery_Date': format_date(row.get('DELIVERY DATE')),
            'SHU': row.get('SHU', ''),
            'DAS': row.get('DAS', ''),
            'MIR': row.get('MIR', ''),
            'AGI': row.get('AGI', ''),
            'Weight_KG': row.get('GWT\n (KG)', ''),
            'CBM': row.get('CBM', ''),
        }
        
        # 최종 목적지 결정
        converted['Final_Site'] = determine_final_site(converted)
        
        # Flow Code 계산
        flow_code, flow_desc, compliance = calculate_flow_code(converted)
        converted['Flow_Code'] = flow_code
        converted['Flow_Desc'] = flow_desc
        converted['Compliance'] = compliance
        
        # 상태 결정
        converted['Status'] = determine_status(converted)
        
        # 지연 여부 계산
        if converted['ETA'] and converted['Status'] != 'Arrived':
            try:
                eta_date = datetime.strptime(converted['ETA'], '%Y-%m-%d')
                if eta_date < TODAY:
                    delay_days = (TODAY - eta_date).days
                    converted['Delay_Days'] = delay_days
                    converted['Remark'] = f"[DELAY {delay_days}일]"
                else:
                    converted['Delay_Days'] = 0
                    converted['Remark'] = ''
            except:
                converted['Delay_Days'] = 0
                converted['Remark'] = ''
        else:
            converted['Delay_Days'] = 0
            converted['Remark'] = ''
        
        converted_rows.append(converted)
    
    # CSV 저장
    fieldnames = ['NO', 'SCT_Ship_No', 'PO_No', 'AWB_No', 'Vendor', 'Item', 
                  'From', 'To', 'Ship_Mode', 'ETA', 'ATA', 'Status',
                  'Final_Site', 'Flow_Code', 'Flow_Desc', 'Compliance',
                  'Customs_Start', 'Customs_Close', 'WH_Date', 'MOSB_Date', 
                  'Delivery_Date', 'Weight_KG', 'CBM', 'Delay_Days', 'Remark']
    
    with open(OUTPUT_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(converted_rows)
    
    # 통계 출력
    stats = {
        "total_records": len(converted_rows),
        "flow_distribution": {},
        "delayed_count": sum(1 for r in converted_rows if r['Delay_Days'] > 0),
        "compliance_fail": sum(1 for r in converted_rows if 'FAIL' in r['Compliance']),
        "output_path": OUTPUT_PATH
    }
    
    for code in range(6):
        stats["flow_distribution"][f"Flow_{code}"] = sum(1 for r in converted_rows if r['Flow_Code'] == code)
    
    print(f"\n✅ 변환 완료: {OUTPUT_PATH}")
    print(f"📊 총 {stats['total_records']}건")
    print(f"📊 지연 건수: {stats['delayed_count']}건")
    print(f"📊 규칙 위반: {stats['compliance_fail']}건")
    print(f"📊 Flow Code 분포:")
    for k, v in stats["flow_distribution"].items():
        print(f"   - {k}: {v}건 ({v/stats['total_records']*100:.1f}%)")
    
    return stats


if __name__ == "__main__":
    import json
    result = convert_hvdc_to_csv()
    if isinstance(result, dict) and result.get('error'):
        print(json.dumps(result, ensure_ascii=False, indent=2))
