#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ontology Stats - 사전 계산된 온톨로지 통계 조회
================================================
- JSON 캐시에서 즉시 로드 (SPARQL 불필요)
- Flow Code, Vendor, 월별 통계
"""

import json
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
DATA_HUB = os.path.join(PROJECT_ROOT, 'data', 'ontology_data_hub', '03_data', 'json')

# 캐시 파일 경로
CACHE = {
    "flow": os.path.join(DATA_HUB, 'gpt_cache', 'cases_by_flow.json'),
    "vendor": os.path.join(DATA_HUB, 'gpt_cache', 'vendor_summary.json'),
    "monthly": os.path.join(DATA_HUB, 'gpt_cache', 'monthly_warehouse_inbound.json'),
    "validation": os.path.join(DATA_HUB, 'validation', 'validation_summary.json'),
    # Reports 추가
    "invoice": os.path.join(DATA_HUB, 'reports', 'invoice_data_summary.json'),
    "lightning": os.path.join(DATA_HUB, 'reports', 'lightning_integrated_stats.json'),
    "lpo": os.path.join(DATA_HUB, 'reports', 'abu_lpo_analysis.json'),
    "whatsapp": os.path.join(DATA_HUB, 'reports', 'abu_whatsapp_analysis.json'),
    # Archive 추가
    "archive_flat": os.path.join(PROJECT_ROOT, 'data', 'ontology_data_hub', '04_archive', 'json', 'hvdc_data_flat.json'),
}


def load_json(path):
    """JSON 파일 로드"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def get_archive_data(filter_key="summary"):
    """아카이브 데이터 (Flat JSON) 조회"""
    data = load_json(CACHE["archive_flat"])
    if not data:
        return {"error": True, "message": "hvdc_data_flat.json 없음"}
    
    cases = data.get("cases", [])
    
    if filter_key == "summary":
        return {
            "query": "ontology-archive-summary",
            "metadata": data.get("metadata"),
            "total_cases": len(cases),
            "sample_case": cases[0] if cases else None
        }
    
    elif filter_key.startswith("search:"):
        keyword = filter_key.split(":")[1].lower()
        results = [
            c for c in cases 
            if keyword in str(c.get("vendor", "")).lower() 
            or keyword in str(c.get("hvdc_code", "")).lower()
            or keyword in str(c.get("case_id", "")).lower()
        ]
        return {
            "query": f"ontology-archive-search:{keyword}",
            "count": len(results),
            "data": results[:20]
        }
    
    return {"error": True, "message": "알 수 없는 필터"}


def get_flow_stats():
    """Flow Code별 통계"""
    data = load_json(CACHE["flow"])
    if not data:
        return {"error": True, "message": "cases_by_flow.json 없음"}
    
    total = sum(d['case_count'] for d in data)
    return {
        "query": "ontology-flow",
        "source": "ontology_data_hub",
        "total_cases": total,
        "by_flow": {d['flow_code']: d['case_count'] for d in data}
    }


def get_validation_stats():
    """검증 통계 (상세)"""
    data = load_json(CACHE["validation"])
    if not data:
        return {"error": True, "message": "validation_summary.json 없음"}
    
    return {
        "query": "ontology-validation",
        "timestamp": data.get("timestamp"),
        "total_triples": data.get("total_triples"),
        "coverage": data["validation_results"].get("coverage_stats"),
        "flow_patterns": data["validation_results"].get("flow_patterns")
    }


def get_vendor_stats():
    """Vendor별 통계"""
    data = load_json(CACHE["vendor"])
    if not data:
        return {"error": True, "message": "vendor_summary.json 없음"}
    
    return {
        "query": "ontology-vendor",
        "data": data
    }


def get_monthly_stats():
    """월별 창고 입고 통계"""
    data = load_json(CACHE["monthly"])
    if not data:
        return {"error": True, "message": "monthly_warehouse_inbound.json 없음"}
    
    return {
        "query": "ontology-monthly",
        "total_records": len(data) if isinstance(data, list) else "object",
        "data": data[:20] if isinstance(data, list) else data
    }


def get_summary():
    """전체 요약"""
    flow = load_json(CACHE["flow"])
    validation = load_json(CACHE["validation"])
    
    return {
        "query": "ontology-summary",
        "source": "ontology_data_hub",
        "total_cases": sum(d['case_count'] for d in flow) if flow else 0,
        "total_triples": validation.get("total_triples") if validation else 0,
        "inbound_coverage": validation["validation_results"]["coverage_stats"]["inbound_coverage_pct"] if validation else 0,
        "flow_distribution": {d['flow_code']: d['case_count'] for d in flow} if flow else {}
    }


def get_invoice_report():
    """Invoice 분석 리포트"""
    data = load_json(CACHE["invoice"])
    if not data:
        return {"error": True, "message": "invoice_data_summary.json 없음"}
    
    return {
        "query": "ontology-invoice",
        "timestamp": data.get("timestamp"),
        "total_invoices": data.get("rdf_data", {}).get("total_invoices"),
        "analysis": data.get("analysis"),
        "comparison": data.get("comparison")
    }


def get_lightning_report():
    """Lightning 통합 리포트"""
    data = load_json(CACHE["lightning"])
    if not data:
        return {"error": True, "message": "lightning_integrated_stats.json 없음"}
    
    return {
        "query": "ontology-lightning",
        "total_vessels": data.get("total_vessels"),
        "total_persons": data.get("total_persons"),
        "total_locations": data.get("total_locations"),
        "total_operations": data.get("total_operations"),
        "total_messages": data.get("total_messages"),
        "timestamp": data.get("analysis_timestamp")
    }


def get_generic_report(key):
    """범용 리포트 로더"""
    data = load_json(CACHE.get(key))
    if not data:
        return {"error": True, "message": f"{key} 리포트 없음"}
    
    if isinstance(data, dict):
        return {"query": f"ontology-{key}", "data": {k: v for k, v in list(data.items())[:10]}}
    return {"query": f"ontology-{key}", "count": len(data), "sample": data[:5]}


def main():
    if len(sys.argv) < 2:
        help_text = """
Ontology Stats - 온톨로지 통계 조회

사용법:
    python check_ontology.py <필터>

필터 옵션:
    summary     - 전체 요약
    flow        - Flow Code별 통계
    validation  - 검증 결과
    vendor      - Vendor별 통계
    monthly     - 월별 창고 입고
    
    invoice     - Invoice 리포트
    lightning   - Lightning 통합 리포트
    lpo         - LPO 분석
    whatsapp    - WhatsApp 분석
    
    archive     - 아카이브(Flat JSON) 요약
    archive:search:키워드 - 아카이브 검색

예시:
    python check_ontology.py summary
    python check_ontology.py lightning
    python check_ontology.py archive
    python check_ontology.py archive:search:Hitachi
"""
        print(help_text)
        return
    
    arg = sys.argv[1].lower()
    
    if arg == "summary":
        result = get_summary()
    elif arg == "flow":
        result = get_flow_stats()
    elif arg == "validation":
        result = get_validation_stats()
    elif arg == "vendor":
        result = get_vendor_stats()
    elif arg == "monthly":
        result = get_monthly_stats()
    elif arg == "invoice":
        result = get_invoice_report()
    elif arg == "lightning":
        result = get_lightning_report()
    elif arg.startswith("archive"):
        if ":" in arg:
            _, cmd, val = arg.split(":", 2)
            result = get_archive_data(f"{cmd}:{val}")
        elif arg == "archive":
             result = get_archive_data("summary")
        else:
             result = get_archive_data("summary")
    elif arg in ["lpo", "whatsapp"]:
        result = get_generic_report(arg)
    else:
        result = get_summary()
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

