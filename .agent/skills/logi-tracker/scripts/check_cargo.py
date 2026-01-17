#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Logi-Tracker v3.0: HVDC-ADOPT 화물 추적 스크립트
=================================================
- Flow Code v3.5 지원 (0-5)
- AGI/DAS 도메인 규칙 검사
- 지연 화물 필터링
- 벌크 화물/LCT 추적
- Port Operations 추적
- Heavy Cargo 필터링
- JSON 형식 출력
"""

import csv
import json
import sys
from datetime import datetime
import os

# 설정: 오늘 날짜 (2026-01-15 기준)
TODAY = datetime(2026, 1, 15)

# 데이터 경로 설정 (스크립트 위치 기준 상대 경로)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'shipping_list.csv')

# Flow Code 설명
FLOW_CODE_DESC = {
    0: "Pre Arrival (통관 대기)",
    1: "Port → Site (직접 배송)",
    2: "Port → WH → Site (창고 경유)",
    3: "Port → MOSB → Site (MOSB 경유)",
    4: "Port → WH → MOSB → Site (전체 체인)",
    5: "Mixed/Incomplete (비정상)"
}


def load_data():
    """CSV 데이터 로드"""
    try:
        with open(DATA_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        return None


def check_delay(row):
    """지연 여부 및 일수 계산"""
    eta_str = row.get('ETA', '')
    if not eta_str or row.get('Status') == 'Arrived':
        return False, 0
    
    try:
        eta_date = datetime.strptime(eta_str, '%Y-%m-%d')
        if eta_date < TODAY:
            return True, (TODAY - eta_date).days
    except ValueError:
        pass
    return False, 0


def filter_by_flow_code(rows, code):
    """Flow Code로 필터링"""
    return [r for r in rows if str(r.get('Flow_Code', '')) == str(code)]


def filter_by_site(rows, site):
    """최종 목적지 사이트로 필터링"""
    site_upper = site.upper()
    return [r for r in rows if site_upper in str(r.get('Final_Site', '')).upper()]


def filter_delayed(rows):
    """지연된 화물만 필터링"""
    results = []
    for row in rows:
        is_delayed, delay_days = check_delay(row)
        if is_delayed:
            row['DelayDays'] = delay_days
            row['Remark'] = f"[DELAY {delay_days}일] {row.get('Remark', '')}"
            results.append(row)
    return results


def filter_compliance_fail(rows):
    """AGI/DAS 규칙 위반 건만 필터링"""
    return [r for r in rows if 'FAIL' in str(r.get('Compliance', ''))]


def filter_at_mosb(rows):
    """현재 MOSB에 있는 화물"""
    return [r for r in rows if r.get('Status') == 'At MOSB']


def filter_in_transit(rows):
    """현재 운송 중인 화물"""
    return [r for r in rows if r.get('Status') == 'In-Transit']


def search_keyword(rows, keyword):
    """키워드로 검색 (PO, AWB, Vendor, Item 등)"""
    keyword_upper = keyword.upper()
    results = []
    for row in rows:
        for value in row.values():
            if keyword_upper in str(value).upper():
                results.append(row)
                break
    return results


def filter_by_port(rows, port_keyword):
    """출발/도착 포트로 필터링"""
    port_upper = port_keyword.upper()
    results = []
    for row in rows:
        from_port = str(row.get('From', '')).upper()
        to_port = str(row.get('To', '')).upper()
        if port_upper in from_port or port_upper in to_port:
            results.append(row)
    return results


def filter_bulk_cargo(rows):
    """벌크 화물만 필터링 (Ship Mode = B)"""
    return [r for r in rows if str(r.get('Ship_Mode', '')).upper() == 'B']


def filter_heavy_cargo(rows, min_weight_kg):
    """중량화물 필터링 (지정 kg 이상)"""
    results = []
    for row in rows:
        try:
            weight = float(row.get('Weight_KG', 0) or 0)
            if weight >= min_weight_kg:
                row['Weight_Tons'] = f"{weight/1000:.2f}t"
                results.append(row)
        except (ValueError, TypeError):
            pass
    # 중량 내림차순 정렬
    results.sort(key=lambda x: float(x.get('Weight_KG', 0) or 0), reverse=True)
    return results


def filter_by_ship_mode(rows, mode):
    """운송 모드로 필터링 (A=Air, B=Bulk, C=Container)"""
    mode_upper = mode.upper()
    return [r for r in rows if str(r.get('Ship_Mode', '')).upper() == mode_upper]


def filter_with_mosb_date(rows):
    """MOSB 경유 기록이 있는 화물"""
    return [r for r in rows if r.get('MOSB_Date') and str(r.get('MOSB_Date')).strip()]


def get_statistics(rows):
    """전체 통계 생성 (확장)"""
    stats = {
        "total": len(rows),
        "by_status": {},
        "by_flow_code": {},
        "by_site": {},
        "by_ship_mode": {},
        "by_port": {},
        "delayed_count": 0,
        "compliance_fail_count": 0,
        "total_weight_tons": 0,
        "total_cbm": 0,
        "heavy_cargo_count": 0,  # 100톤 이상
        "mosb_transit_count": 0
    }
    
    for row in rows:
        # 상태별
        status = row.get('Status', 'Unknown')
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        
        # Flow Code별
        flow = f"Flow_{row.get('Flow_Code', '?')}"
        stats["by_flow_code"][flow] = stats["by_flow_code"].get(flow, 0) + 1
        
        # 사이트별
        site = row.get('Final_Site', 'Unknown')
        stats["by_site"][site] = stats["by_site"].get(site, 0) + 1
        
        # 운송 모드별
        mode = row.get('Ship_Mode', 'Unknown')
        mode_name = {'A': 'Air', 'B': 'Bulk', 'C': 'Container'}.get(mode, mode)
        stats["by_ship_mode"][mode_name] = stats["by_ship_mode"].get(mode_name, 0) + 1
        
        # 도착 포트별
        to_port = row.get('To', 'Unknown')
        if to_port and str(to_port).strip():
            stats["by_port"][to_port] = stats["by_port"].get(to_port, 0) + 1
        
        # 지연 건수
        is_delayed, _ = check_delay(row)
        if is_delayed:
            stats["delayed_count"] += 1
        
        # 규칙 위반
        if 'FAIL' in str(row.get('Compliance', '')):
            stats["compliance_fail_count"] += 1
        
        # 중량/체적 합계
        try:
            weight = float(row.get('Weight_KG', 0) or 0)
            stats["total_weight_tons"] += weight / 1000
            if weight >= 100000:  # 100톤 이상
                stats["heavy_cargo_count"] += 1
        except:
            pass
        
        try:
            cbm = float(row.get('CBM', 0) or 0)
            stats["total_cbm"] += cbm
        except:
            pass
        
        # MOSB 경유 건수
        if row.get('MOSB_Date') and str(row.get('MOSB_Date')).strip():
            stats["mosb_transit_count"] += 1
    
    # 소수점 정리
    stats["total_weight_tons"] = round(stats["total_weight_tons"], 2)
    stats["total_cbm"] = round(stats["total_cbm"], 2)
    
    return stats


def check_status(filter_key="all"):
    """
    화물 상태를 조회하고 필터링합니다.
    
    Args:
        filter_key (str): 필터 조건
            - "all": 전체 조회
            - "delay": 지연 건만
            - "flow:0" ~ "flow:5": Flow Code 필터
            - "site:agi", "site:das", "site:mir", "site:shu": 사이트별
            - "compliance": 규칙 위반 건
            - "mosb": MOSB 대기 건
            - "transit": 운송 중
            - "stats": 통계만
            - 기타: 키워드 검색
    
    Returns:
        dict: 조회 결과
    """
    rows = load_data()
    
    if rows is None:
        return {
            "error": True,
            "message": f"shipping_list.csv 파일을 찾을 수 없습니다.\n경로: {DATA_PATH}\n\n먼저 convert_hvdc_status.py를 실행하세요."
        }
    
    filter_lower = filter_key.lower()
    
    # 통계 조회
    if filter_lower == "stats":
        return {
            "query": "statistics",
            "query_time": TODAY.strftime('%Y-%m-%d'),
            "statistics": get_statistics(rows)
        }
    
    # Flow Code 필터
    if filter_lower.startswith("flow:"):
        code = filter_key.split(":")[1]
        results = filter_by_flow_code(rows, code)
        flow_desc = FLOW_CODE_DESC.get(int(code), "Unknown")
    
    # 사이트 필터
    elif filter_lower.startswith("site:"):
        site = filter_key.split(":")[1]
        results = filter_by_site(rows, site)
        flow_desc = None
    
    # 특수 필터
    elif filter_lower == "delay":
        results = filter_delayed(rows)
        flow_desc = None
    
    elif filter_lower == "compliance":
        results = filter_compliance_fail(rows)
        flow_desc = None
    
    elif filter_lower == "mosb":
        results = filter_at_mosb(rows)
        flow_desc = None
    
    elif filter_lower == "transit":
        results = filter_in_transit(rows)
        flow_desc = None
    
    # Port 필터 (신규)
    elif filter_lower.startswith("port:"):
        port = filter_key.split(":")[1]
        results = filter_by_port(rows, port)
        flow_desc = None
    
    # Bulk 화물 필터 (신규)
    elif filter_lower == "bulk":
        results = filter_bulk_cargo(rows)
        flow_desc = None
    
    # Heavy 화물 필터 (신규)
    elif filter_lower.startswith("heavy:"):
        try:
            min_tons = float(filter_key.split(":")[1])
            min_kg = min_tons * 1000
        except:
            min_kg = 100000  # 기본 100톤
        results = filter_heavy_cargo(rows, min_kg)
        flow_desc = None
    
    # 운송 모드 필터 (신규)
    elif filter_lower.startswith("mode:"):
        mode = filter_key.split(":")[1]
        results = filter_by_ship_mode(rows, mode)
        flow_desc = None
    
    # MOSB 경유 화물 (신규)
    elif filter_lower == "mosb-transit":
        results = filter_with_mosb_date(rows)
        flow_desc = None
    
    elif filter_lower == "all":
        results = rows
        flow_desc = None
    
    else:
        # 키워드 검색
        results = search_keyword(rows, filter_key)
        flow_desc = None
    
    # 결과 포맷팅
    summary = {
        "query": filter_key,
        "total_count": len(results),
        "query_time": TODAY.strftime('%Y-%m-%d'),
    }
    
    if flow_desc:
        summary["flow_description"] = flow_desc
    
    # 결과가 너무 많으면 요약만
    if len(results) > 50:
        summary["note"] = f"결과가 {len(results)}건입니다. 처음 50건만 표시합니다."
        summary["data"] = results[:50]
    else:
        summary["data"] = results
    
    return summary


def main():
    """메인 실행 함수"""
    if len(sys.argv) < 2:
        # 도움말 출력
        help_text = """
Logi-Tracker v2.0 - HVDC 화물 추적 도구

사용법:
    python check_cargo.py <필터>

필터 옵션:
    all         - 전체 화물 조회
    delay       - 지연된 화물만
    stats       - 통계 요약
    
    flow:0      - Flow 0 (Pre Arrival)
    flow:1      - Flow 1 (Port → Site)
    flow:2      - Flow 2 (Port → WH → Site)
    flow:3      - Flow 3 (Port → MOSB → Site)
    flow:4      - Flow 4 (Port → WH → MOSB → Site)
    flow:5      - Flow 5 (Incomplete)
    
    site:agi    - AGI 목적지
    site:das    - DAS 목적지
    site:mir    - MIR 목적지
    site:shu    - SHU 목적지
    
    compliance  - AGI/DAS 규칙 위반
    mosb        - MOSB 대기 중
    transit     - 운송 중
    
    port:khalifa - Khalifa Port 화물
    port:zayed   - Zayed Port 화물
    bulk         - 벌크 화물 (Ship Mode = B)
    heavy:100    - 100톤 이상 중량화물
    mode:a       - Air (A), Bulk (B), Container (C)
    mosb-transit - MOSB 경유 기록 있는 화물
    
    <키워드>    - PO/AWB/Vendor 등 검색

예시:
    python check_cargo.py delay
    python check_cargo.py flow:3
    python check_cargo.py site:agi
    python check_cargo.py bulk
    python check_cargo.py heavy:100
    python check_cargo.py port:khalifa
"""
        print(help_text)
        return
    
    arg = sys.argv[1]
    data = check_status(arg)
    
    # JSON 형태로 출력
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
