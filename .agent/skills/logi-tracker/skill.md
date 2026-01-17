# Logi-Tracker Skill v3.2

## Modules

### 1. Cargo Tracker (`check_cargo.py`)
```bash
python check_cargo.py <필터>
```
| 필터 | 설명 |
|------|------|
| `stats` | 전체 통계 |
| `bulk` | 벌크 화물 |
| `heavy:100` | 100톤+ |
| `port:khalifa` | Khalifa Port |
| `site:agi` | AGI 목적지 |

### 2. Invoice Tracker (`check_invoice.py`)
```bash
python check_invoice.py <필터>
```
| 필터 | 설명 |
|------|------|
| `summary` | Invoice 요약 |
| `cost-stats` | Cost Center 통계 |
| `price-stats` | Price Center 통계 |
| `cost-guard` | 비용 이상치 탐지 (PRISM) |
| `invoice:OFCO-xxx` | Invoice 검색 |

### 3. Voyage Tracker (`check_voyage.py`) - v3.2 신규
```bash
python check_voyage.py <필터>
```
| 필터 | 설명 |
|------|------|
| `summary` | Voyage 요약 |
| `voyage:J71` | 화물+Invoice 통합 검색 |
| `voyage:HE` | HE 화물 494건 |

### 4. Ontology Tracker (`check_ontology.py`) - v3.3 신규
```bash
python check_ontology.py <필터>
```
| 필터 | 설명 |
|------|------|
| `summary` | 온톨로지 요약 |
| `flow` | Flow Code 통계 |
| `validation` | 데이터 검증 결과 |
| `lightning` | Lightning 리포트 |
| `invoice` | Invoice 리포트 |
| `archive` | 아카이브 요약 |
| `archive:search:xxx` | 아카이브 검색 |

### 5. TTL Parser (`check_ttl.py`) - v3.4 신규
```bash
python check_ttl.py <명령>
```
| 명령 | 설명 |
|------|------|
| `list` | TTL 파일 목록 |
| `stats:hvdc` | HVDC TTL 통계 |
| `stats:lightning` | Lightning TTL 통계 |

## Data Sources
- **Live**: `shipping_list.csv`, `ofco_invoice.csv`
- **Ontology Hub**: `cases_by_flow.json`, `lightning_integrated_system.ttl` 등
- **Archive**: `hvdc_data_flat.json` (3MB)
