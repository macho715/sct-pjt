# Logi-Tracker 통합 사용 가이드

## 1. 📦 화물 추적 (Cargo)
**스크립트**: `.agent/skills/logi-tracker/scripts/check_cargo.py`

| 목적 | 명령어 |
|------|--------|
| **전체 통계** | `python check_cargo.py stats` |
| **벌크 화물** | `python check_cargo.py bulk` |
| **중량화물 (100t+)** | `python check_cargo.py heavy:100` |
| **항구별 조희** | `python check_cargo.py port:khalifa` |
| **목적지 조회** | `python check_cargo.py site:agi` |
| **지연 화물** | `python check_cargo.py delay` |

---

## 2. 💰 비용/청구서 (Invoice)
**스크립트**: `.agent/skills/logi-tracker/scripts/check_invoice.py`

| 목적 | 명령어 |
|------|--------|
| **청구서 요약** | `python check_invoice.py summary` |
| **비용 통계 (Cost Center)** | `python check_invoice.py cost-stats` |
| **비용 통계 (Price Center)** | `python check_invoice.py price-stats` |
| **특정 Invoice 검색** | `python check_invoice.py invoice:OFCO-INV-1024` |

---

## 3. 🚢 통합 조회 (Voyage)
**스크립트**: `.agent/skills/logi-tracker/scripts/check_voyage.py`

| 목적 | 명령어 |
|------|--------|
| **화물+비용 통합 연결** | `python check_voyage.py voyage:J71` |
| **특정 선박 화물** | `python check_voyage.py voyage:HE` |

---

## 4. 🧠 지식/온톨로지 (Knowledge)
**스크립트**: `.agent/skills/logi-tracker/scripts/check_ontology.py`
**스크립트**: `.agent/skills/logi-tracker/scripts/check_ttl.py`

| 목적 | 명령어 |
|------|--------|
| **Lightning 리포트** | `python check_ontology.py lightning` |
| **과거 데이터 검색** | `python check_ontology.py archive:search:Hitachi` |
| **TTL 파일 분석** | `python check_ttl.py stats:lightning` |

---

## 5. 📝 자동 리포트 (Auto-Reporter)
**스크립트**: `.agent/skills/auto-reporter/scripts/write_log.py`

| 목적 | 명령어 |
|------|--------|
| **일일 리포트 생성** | `python .agent/skills/auto-reporter/scripts/write_log.py --site=DAS --weather="Windy"` |
| **옵션: 이슈 추가** | `--issue="Crane Breakdown"` |
| **옵션: 계획 추가** | `--plan="Reschedule LCT"` |

**설정 (선박 스케줄):**
- **파일**: `data/vessel_schedule.csv`
- **형식**: `Date,Vessel,Status,Location,Activity`
- **자동화**: 오늘 날짜의 선박(Busra, JPT71) 상태를 자동 반영합니다.
