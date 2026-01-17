# Auto-Reporter Skill

## Description
HVDC-ADOPT 프로젝트의 일일 물류 리포트(Daily Logistics Report) 초안을 작성하는 스킬입니다.
CONSOLIDATED-09 문서에 정의된 표준 포맷을 사용합니다.

## When to use
- "오늘 DAS 현장 리포트 써줘"
- "일일 리포트 작성해(Make daily report)"
- "날씨는 맑음, 특이사항은 크레인 고장이라고 기록해줘"

## Execution
- **Script:** `python .agent/skills/auto-reporter/scripts/write_log.py`
- **Arguments:**
    - `--site`: "DAS", "MIR", "SHU", "AGI" (Project Sites)
    - `--weather`: 날씨 및 해상 상태 (예: "Windy, 2.5m waves")
    - `--issue`: 주요 이슈 사항 (One-liner)
    - `--plan`: 익일 계획

## Setup (Vessel Schedule)
- **File:** `data/vessel_schedule.csv`
- **Format:** `Date,Vessel,Status,Location,Activity`
- **Automation:** 날짜와 선박명이 일치하면 리포트에 자동 기입됩니다.
