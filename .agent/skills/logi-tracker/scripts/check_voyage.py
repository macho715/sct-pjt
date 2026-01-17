#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Voyage Tracker - 화물+Invoice 통합 조회
========================================
- Voyage 번호로 화물+Invoice 통합 검색
- SCT Ship No / Voyage No 연동
"""

import csv
import json
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
CARGO_PATH = os.path.join(PROJECT_ROOT, 'data', 'shipping_list.csv')
INVOICE_PATH = os.path.join(PROJECT_ROOT, 'data', 'ofco_invoice.csv')


def load_csv(path):
    """CSV 로드"""
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return None


def search_voyage_unified(voyage_key):
    """Voyage 통합 검색 (화물 + Invoice)"""
    cargo_data = load_csv(CARGO_PATH)
    invoice_data = load_csv(INVOICE_PATH)
    
    if not cargo_data:
        return {"error": True, "message": "shipping_list.csv 없음"}
    if not invoice_data:
        return {"error": True, "message": "ofco_invoice.csv 없음"}
    
    voyage_upper = voyage_key.upper()
    
    # 화물 검색 (SCT_Ship_No에서 검색)
    cargo_results = []
    for row in cargo_data:
        sct_no = str(row.get('SCT_Ship_No', '')).upper()
        if voyage_upper in sct_no:
            cargo_results.append({
                "SCT_Ship_No": row.get('SCT_Ship_No'),
                "PO_No": row.get('PO_No'),
                "Vendor": row.get('Vendor'),
                "Item": row.get('Item'),
                "Final_Site": row.get('Final_Site'),
                "Status": row.get('Status'),
                "Weight_KG": row.get('Weight_KG'),
                "Flow_Code": row.get('Flow_Code')
            })
    
    # Invoice 검색 (Voyage No에서 검색)
    invoice_results = []
    total_invoice_amount = 0
    for row in invoice_data:
        voyage_no = str(row.get('Voyage No', '')).upper()
        if voyage_upper in voyage_no:
            try:
                amount = float(row.get('TOTAL_AMOUNT', 0) or 0)
            except:
                amount = 0
            total_invoice_amount += amount
            invoice_results.append({
                "Voyage_No": row.get('Voyage No'),
                "Invoice_No": row.get('INVOICE NUMBER'),
                "Subject": row.get('SUBJECT'),
                "Cost_Center_A": row.get('COST CENTER A'),
                "Price_Center": row.get('PRICE CENTER'),
                "Amount": amount
            })
    
    return {
        "query": f"voyage:{voyage_key}",
        "cargo": {
            "count": len(cargo_results),
            "data": cargo_results[:20]
        },
        "invoice": {
            "count": len(invoice_results),
            "total_amount": round(total_invoice_amount, 2),
            "data": invoice_results[:20]
        }
    }


def get_voyage_summary():
    """Voyage 전체 요약"""
    cargo_data = load_csv(CARGO_PATH)
    invoice_data = load_csv(INVOICE_PATH)
    
    if not cargo_data or not invoice_data:
        return {"error": True, "message": "데이터 파일 없음"}
    
    # Voyage 패턴 추출
    cargo_voyages = set()
    for row in cargo_data:
        sct = row.get('SCT_Ship_No', '')
        if sct:
            # HVDC-ADOPT-XXX-YYYY 형식에서 XXX 추출
            parts = sct.split('-')
            if len(parts) >= 3:
                cargo_voyages.add(parts[2])  # HE, SEI, PPL, SCT 등
    
    invoice_voyages = set()
    for row in invoice_data:
        voyage = row.get('Voyage No', '')
        if voyage:
            invoice_voyages.add(voyage)
    
    return {
        "query": "voyage-summary",
        "cargo_voyage_codes": sorted(list(cargo_voyages)),
        "invoice_voyage_codes": sorted(list(invoice_voyages))[:20],
        "total_cargo": len(cargo_data),
        "total_invoices": len(invoice_data)
    }


def main():
    if len(sys.argv) < 2:
        help_text = """
Voyage Tracker - 화물+Invoice 통합 조회

사용법:
    python check_voyage.py <필터>

필터 옵션:
    summary          - Voyage 요약
    voyage:J71       - Voyage 번호로 통합 검색
    voyage:HE        - HE 관련 화물+Invoice 검색
    
예시:
    python check_voyage.py summary
    python check_voyage.py voyage:J71-01
    python check_voyage.py voyage:HE
"""
        print(help_text)
        return
    
    arg = sys.argv[1].lower()
    
    if arg == "summary":
        result = get_voyage_summary()
    elif arg.startswith("voyage:"):
        voyage_key = sys.argv[1].split(":")[1]
        result = search_voyage_unified(voyage_key)
    else:
        result = search_voyage_unified(arg)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
