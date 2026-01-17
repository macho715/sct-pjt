#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TTL Parser - RDFLib 기반 온톨로지 데이터 조회
=============================================
- TTL 파일에서 엔티티 추출
- SPARQL 쿼리 지원
- 통계 생성
"""

import json
import sys
import os

try:
    from rdflib import Graph, Namespace
    from rdflib.namespace import RDF, RDFS, XSD
    HAS_RDFLIB = True
except ImportError:
    HAS_RDFLIB = False

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))
TTL_DIR = os.path.join(PROJECT_ROOT, 'data', 'ontology_data_hub', '03_data', 'ttl')

# TTL 파일 경로
TTL_FILES = {
    "hvdc": os.path.join(TTL_DIR, 'current', 'hvdc_status_v35.ttl'),
    "lightning": os.path.join(TTL_DIR, 'specialized', 'lightning_integrated_system.ttl'),
    "abu": os.path.join(TTL_DIR, 'specialized', 'abu_integrated_system.ttl'),
    "lpo": os.path.join(TTL_DIR, 'specialized', 'abu_lpo_data.ttl'),
}


def load_graph(ttl_path):
    """TTL 파일을 RDF Graph로 로드"""
    if not HAS_RDFLIB:
        return None
    
    g = Graph()
    try:
        g.parse(ttl_path, format='turtle')
        return g
    except Exception as e:
        return None


def get_ttl_stats(key):
    """TTL 파일 통계"""
    if key not in TTL_FILES:
        return {"error": True, "message": f"알 수 없는 TTL: {key}. 가능: hvdc, lightning, abu, lpo"}
    
    path = TTL_FILES[key]
    if not os.path.exists(path):
        return {"error": True, "message": f"파일 없음: {path}"}
    
    if not HAS_RDFLIB:
        # 파일 크기만 반환
        size = os.path.getsize(path)
        return {
            "query": f"ttl-{key}",
            "file": os.path.basename(path),
            "size_kb": round(size / 1024, 2),
            "note": "RDFLib 없음 - 기본 정보만"
        }
    
    g = load_graph(path)
    if not g:
        return {"error": True, "message": "TTL 파싱 실패"}
    
    # 기본 통계
    stats = {
        "query": f"ttl-{key}",
        "file": os.path.basename(path),
        "total_triples": len(g),
        "subjects": len(set(g.subjects())),
        "predicates": len(set(g.predicates())),
        "objects": len(set(g.objects())),
    }
    
    # 네임스페이스
    stats["namespaces"] = {str(prefix): str(ns) for prefix, ns in g.namespaces() if prefix}
    
    return stats


def query_ttl(key, sparql_query):
    """TTL에 SPARQL 쿼리 실행"""
    if not HAS_RDFLIB:
        return {"error": True, "message": "RDFLib 필요"}
    
    if key not in TTL_FILES:
        return {"error": True, "message": f"알 수 없는 TTL: {key}"}
    
    g = load_graph(TTL_FILES[key])
    if not g:
        return {"error": True, "message": "TTL 로드 실패"}
    
    try:
        results = g.query(sparql_query)
        data = []
        for row in results:
            data.append({str(var): str(val) for var, val in zip(results.vars, row)})
        return {
            "query": f"sparql-{key}",
            "count": len(data),
            "data": data[:20]
        }
    except Exception as e:
        return {"error": True, "message": f"SPARQL 오류: {str(e)}"}


def list_ttl_files():
    """사용 가능한 TTL 파일 목록"""
    result = {"query": "ttl-list", "files": {}}
    
    for key, path in TTL_FILES.items():
        if os.path.exists(path):
            size = os.path.getsize(path)
            result["files"][key] = {
                "path": os.path.basename(path),
                "size_kb": round(size / 1024, 2)
            }
    
    return result


def main():
    if len(sys.argv) < 2:
        help_text = """
TTL Parser - 온톨로지 TTL 파일 조회

사용법:
    python check_ttl.py <명령>

명령어:
    list         - TTL 파일 목록
    stats:hvdc   - HVDC TTL 통계
    stats:lightning - Lightning TTL 통계
    stats:abu    - ABU TTL 통계
    stats:lpo    - LPO TTL 통계

예시:
    python check_ttl.py list
    python check_ttl.py stats:hvdc
"""
        print(help_text)
        return
    
    arg = sys.argv[1].lower()
    
    if arg == "list":
        result = list_ttl_files()
    elif arg.startswith("stats:"):
        key = arg.split(":")[1]
        result = get_ttl_stats(key)
    else:
        result = list_ttl_files()
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
