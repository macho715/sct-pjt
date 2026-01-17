#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OFCO Invoice Tracker
====================
- Invoice 번호 검색
- Cost Center 분석
- Price Center 통계
- Voyage 연동
"""

import csv
import json
import sys
import os
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
INVOICE_PATH = os.path.join(PROJECT_ROOT, 'data', 'ofco_invoice.csv')


def load_invoices():
    """Invoice CSV 로드"""
    try:
        with open(INVOICE_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        return None


def search_invoice(invoice_no):
    """Invoice 번호로 검색"""
    rows = load_invoices()
    if not rows:
        return {"error": True, "message": "ofco_invoice.csv 없음. convert_ofco_invoice.py 먼저 실행"}
    
    results = [r for r in rows if invoice_no.upper() in str(r.get('INVOICE NUMBER', '')).upper()]
    return {
        "query": f"invoice:{invoice_no}",
        "total_count": len(results),
        "data": results[:50]
    }


def search_voyage(voyage_no):
    """Voyage 번호로 검색"""
    rows = load_invoices()
    if not rows:
        return {"error": True, "message": "ofco_invoice.csv 없음"}
    
    results = [r for r in rows if voyage_no.upper() in str(r.get('Voyage No', '')).upper()]
    return {
        "query": f"voyage:{voyage_no}",
        "total_count": len(results),
        "data": results[:50]
    }


def get_cost_center_stats():
    """Cost Center A 통계"""
    rows = load_invoices()
    if not rows:
        return {"error": True, "message": "ofco_invoice.csv 없음"}
    
    stats = defaultdict(lambda: {"count": 0, "total_amount": 0})
    
    for row in rows:
        center = row.get('COST CENTER A', 'Unknown')
        stats[center]["count"] += 1
        try:
            amount = float(row.get('TOTAL_AMOUNT', 0) or 0)
            stats[center]["total_amount"] += amount
        except:
            pass
    
    # 정렬
    sorted_stats = dict(sorted(stats.items(), key=lambda x: x[1]["total_amount"], reverse=True))
    
    return {
        "query": "cost-stats",
        "data": sorted_stats
    }


def get_price_center_stats():
    """Price Center 통계"""
    rows = load_invoices()
    if not rows:
        return {"error": True, "message": "ofco_invoice.csv 없음"}
    
    stats = defaultdict(lambda: {"count": 0, "total_amount": 0})
    
    for row in rows:
        center = row.get('PRICE CENTER', 'Unknown')
        stats[center]["count"] += 1
        try:
            amount = float(row.get('TOTAL_AMOUNT', 0) or 0)
            stats[center]["total_amount"] += amount
        except:
            pass
    
    sorted_stats = dict(sorted(stats.items(), key=lambda x: x[1]["total_amount"], reverse=True))
    
    return {
        "query": "price-stats",
        "data": sorted_stats
    }


def get_invoice_summary():
    """전체 Invoice 요약"""
    rows = load_invoices()
    if not rows:
        return {"error": True, "message": "ofco_invoice.csv 없음"}
    
    total_amount = 0
    invoices = set()
    voyages = set()
    
    for row in rows:
        invoices.add(row.get('INVOICE NUMBER', ''))
        voyages.add(row.get('Voyage No', ''))
        try:
            total_amount += float(row.get('TOTAL_AMOUNT', 0) or 0)
        except:
            pass
    
    return {
        "query": "invoice-summary",
        "total_records": len(rows),
        "unique_invoices": len(invoices),
        "unique_voyages": len(voyages),
        "total_amount": round(total_amount, 2)
    }


def get_cost_guard_report():
    """
    Cost Guard Analysis (CONSOLIDATED-05)
    - Price Center별 평균 단가 계산
    - 허용 오차(Tolerance)를 벗어난 이상치(Outlier) 탐지
    - PRISM.KERNEL 포맷으로 리포팅
    """
    invoice_data = load_invoices()
    if not invoice_data:
        return {"error": True, "message": "데이터 없음"}

    # 1. Price Center별 통계 산출 (Baseline)
    price_stats = defaultdict(list)
    for row in invoice_data:
        pc = row.get('PRICE CENTER', 'Unknown')
        try:
            amt = float(row.get('TOTAL_AMOUNT', 0) or 0)
            if amt > 0:
                price_stats[pc].append(amt)
        except:
            continue
    
    baselines = {}
    for pc, amounts in price_stats.items():
        if len(amounts) > 2: # 최소 3개 이상 표본이 있을 때만 기준 설정
            avg = sum(amounts) / len(amounts)
            baselines[pc] = avg

    # 2. 이상치 탐지 (Simulation of Tolerance Verification)
    anomalies = []
    TOLERANCE_PCT = 0.50 # 50% 이상 차이나면 WARNING (Demo용, 실제는 3~10%)

    for row in invoice_data:
        pc = row.get('PRICE CENTER', 'Unknown')
        inv_no = row.get('INVOICE NUMBER')
        voy_no = row.get('Voyage No')
        
        if pc in baselines:
            try:
                amt = float(row.get('TOTAL_AMOUNT', 0) or 0)
                ref_rate = baselines[pc]
                
                # Delta Calculation
                if ref_rate > 0:
                    delta = (amt - ref_rate) / ref_rate
                    delta_pct = delta * 100
                    
                    if abs(delta) > TOLERANCE_PCT:
                        # Verdict Logic
                        verdict = "WARN" if abs(delta) < 1.0 else "CRITICAL"
                        
                        # PRISM.KERNEL Recap Format
                        recap = f"{inv_no} | {pc} | AED {amt:,.2f} | Δ% {delta_pct:+.1f}% | VERDICT: {verdict}"
                        
                        anomalies.append({
                            "recap": recap,
                            "artifact": {
                                "invoiceId": inv_no,
                                "voyageNo": voy_no,
                                "priceCenter": pc,
                                "amount": amt,
                                "refAvgAmount": round(ref_rate, 2),
                                "riskResult": {
                                    "deltaPercent": round(delta_pct, 2),
                                    "verdict": verdict
                                }
                            }
                        })
            except:
                continue
                
    # Sort by criticality (High delta first)
    anomalies.sort(key=lambda x: abs(x['artifact']['riskResult']['deltaPercent']), reverse=True)

    return {
        "query": "cost-guard",
        "description": "Cost Guard Analysis based on CON-05 (Automatic Outlier Detection)",
        "baselines_established": len(baselines),
        "anomalies_detected": len(anomalies),
        "top_risks_prism": anomalies[:20] # Top 20 Risks
    }


def check_invoice(filter_key="summary"):
    """Invoice 조회 메인 함수"""
    filter_lower = filter_key.lower()
    
    if filter_lower == "summary" or filter_lower == "stats":
        return get_invoice_summary()
    
    elif filter_lower == "cost-guard":
        return get_cost_guard_report()
    
    elif filter_lower.startswith("invoice:"):
        inv_no = filter_key.split(":")[1]
        return search_invoice(inv_no)
    
    elif filter_lower.startswith("voyage:"):
        voy_no = filter_key.split(":")[1]
        return search_voyage(voy_no)
    
    elif filter_lower == "cost-stats":
        return get_cost_center_stats()
    
    elif filter_lower == "price-stats":
        return get_price_center_stats()
    
    else:
        # 키워드 검색
        rows = load_invoices()
        if not rows:
            return {"error": True, "message": "ofco_invoice.csv 없음"}
        
        results = []
        for row in rows:
            for v in row.values():
                if filter_key.upper() in str(v).upper():
                    results.append(row)
                    break
        
        return {
            "query": filter_key,
            "total_count": len(results),
            "data": results[:50]
        }


def main():
    if len(sys.argv) < 2:
        help_text = """
OFCO Invoice Tracker

사용법:
    python check_invoice.py <필터>

필터 옵션:
    summary       - 전체 요약
    cost-stats    - Cost Center A별 통계
    price-stats   - Price Center별 통계
    cost-guard    - 비용 이상치 탐지 (Cost Guard)
    
    invoice:OFCO-INV-xxx - Invoice 번호 검색
    voyage:J71-01        - Voyage 번호 검색
    
    <키워드>       - 자유 검색

예시:
    python check_invoice.py summary
    python check_invoice.py cost-stats
    python check_invoice.py cost-guard
    python check_invoice.py invoice:OFCO-INV-1024
    python check_invoice.py voyage:J71
"""
        print(help_text)
        return
    
    arg = sys.argv[1]
    data = check_invoice(arg)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
