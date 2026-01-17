#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OFCO Invoice Converter & Analyzer
==================================
- OFCO Invoice Excel → CSV 변환
- Cost Center 분석
- Price Center 통계
"""

import os
import sys
import csv
from datetime import datetime

try:
    import pandas as pd
except ImportError:
    print('{"error": true, "message": "pandas 라이브러리 필요"}')
    sys.exit(1)

# 경로 설정
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
EXCEL_PATH = os.path.join(PROJECT_ROOT, 'ofco.xlsx')  # 새 파일 경로
OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'data', 'ofco_invoice.csv')


def convert_ofco_to_csv():
    """OFCO Invoice Excel → CSV 변환"""
    print(f"📂 OFCO Invoice 읽는 중: {EXCEL_PATH}")
    
    try:
        df = pd.read_excel(EXCEL_PATH)
    except FileNotFoundError:
        return {"error": True, "message": f"파일 없음: {EXCEL_PATH}"}
    
    print(f"✅ {len(df)}건 로드됨")
    
    # 핵심 컬럼 선택
    key_columns = [
        '전체 순번', '청구 회차', 'NO', 'Voyage No', 'SUBJECT',
        'INVOICE NUMBER', 'INVOICE DATE', 'INVOICE DATE_YEAR_MONTH',
        'COST MAIN', 'COST CENTER A', 'COST CENTER B', 'PRICE CENTER'
    ]
    
    # AMOUNT 컬럼 추가
    amount_cols = [c for c in df.columns if 'AMOUNT' in str(c)]
    
    # 전각 공백 "　" 및 빈 값을 0으로 변환
    for col in amount_cols:
        if col in df.columns:
            df[col] = df[col].replace(['　', ' ', '', None], 0)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # 선택된 컬럼만 추출
    available_cols = [c for c in key_columns if c in df.columns]
    available_cols.extend([c for c in amount_cols if c in df.columns])
    
    df_export = df[available_cols].copy()
    
    # 총 금액 계산
    df_export['TOTAL_AMOUNT'] = df[amount_cols].sum(axis=1)
    
    # CSV 저장
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df_export.to_csv(OUTPUT_PATH, index=False, encoding='utf-8')
    
    # 통계
    stats = {
        "total_records": len(df_export),
        "total_amount": df_export['TOTAL_AMOUNT'].sum(),
        "cost_center_a": df['COST CENTER A'].value_counts().to_dict() if 'COST CENTER A' in df.columns else {},
        "price_center": df['PRICE CENTER'].value_counts().head(10).to_dict() if 'PRICE CENTER' in df.columns else {},
        "output_path": OUTPUT_PATH
    }
    
    print(f"\n✅ 변환 완료: {OUTPUT_PATH}")
    print(f"📊 총 {stats['total_records']}건")
    print(f"📊 총 금액: {stats['total_amount']:,.2f} AED")
    
    return stats


if __name__ == "__main__":
    import json
    result = convert_ofco_to_csv()
    if isinstance(result, dict) and result.get('error'):
        print(json.dumps(result, ensure_ascii=False))
