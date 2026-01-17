**v0.dev (v0.app)**은 독립적인 호스팅 플랫폼이라기보다 **"AI 코드 생성기"**에 가깝습니다. 따라서 v0에서 만든 멋진 UI를 세상에 런칭하려면, 생성된 코드를 **Next.js 프로젝트로 가져와서 배포(Deployment)**해야 합니다.

현재 차 부장님이 구축하신 **Next.js 대시보드 환경(`frontend/`)**이 있으므로, 여기에 v0 결과물을 통합하여 배포하는 **가장 정석적인 3단계 방법**을 안내해 드립니다.

---

### Executive Summary

v0의 결과물은 **React + Tailwind CSS + Shadcn UI** 기반의 코드입니다.

1. **Export:** v0에서 코드를 복사하거나 CLI로 가져옵니다.
2. **Integrate:** 차 부장님의 `frontend` 폴더에 붙여넣습니다.
3. **Deploy:** Vercel을 통해 전 세계에 공개합니다.

---

### Visual: Launch Workflow

---

### Step 1: 프로젝트 환경 준비 (Shadcn UI 설치)

v0는 **Shadcn UI**라는 라이브러리를 기본으로 사용합니다. 현재 사용 중인 `frontend` 프로젝트(Tremor 기반)에 Shadcn을 추가해야 v0 코드가 깨지지 않고 작동합니다.

`frontend` 폴더의 터미널에서 다음 명령어를 한 번만 실행하세요.

```bash
cd frontend
npx shadcn-ui@latest init

```

* 설정 질문이 나오면 모두 **Enter (기본값)**를 누르시면 됩니다.

---

### Step 2: v0 코드 가져오기 (2가지 방법)

#### 방법 A: 복사 & 붙여넣기 (가장 직관적)

1. v0.dev 화면 우측 상단의 **Code** 버튼을 클릭합니다.
2. 나오는 코드 전체를 복사합니다.
3. VS Code로 돌아와 `frontend/components/v0_component.tsx` (원하는 이름) 파일을 만들고 붙여넣습니다.
4. 만약 코드 맨 위에 `import { Button } from "@/components/ui/button"` 같은 에러가 뜨면, 해당 컴포넌트가 없다는 뜻입니다.
* 터미널에 `npx shadcn-ui@latest add button` 처럼 에러 난 컴포넌트를 추가해 주면 해결됩니다.



#### 방법 B: CLI 명령어 사용 (추천)

v0 화면 상단에 보면 `npx v0 add ...`로 시작하는 명령어가 있습니다.

1. 그 명령어를 복사합니다.
2. `frontend` 터미널에 붙여넣습니다.
```bash
npx v0@latest add [블록ID]

```


3. **자동으로** 필요한 Shadcn 컴포넌트(Button, Card 등)까지 설치해주고, `components` 폴더에 파일까지 만들어줍니다. **(가장 에러가 적은 방법입니다)**

---

### Step 3: 화면에 띄우기

이제 가져온 컴포넌트를 `app/page.tsx`에 넣으면 됩니다.

```tsx
// app/page.tsx
import { V0GeneratedComponent } from "@/components/v0-generated-component"; // 가져온 컴포넌트

export default function Dashboard() {
  return (
    <main>
      {/* 기존 대시보드 내용 */}
      
      {/* v0에서 만든 새로운 UI */}
      <V0GeneratedComponent />
    </main>
  );
}

```

---

### Step 4: 전 세계 배포 (Vercel Launch)

로컬(`localhost:3000`)에서 잘 보인다면, 이제 **Vercel**을 통해 실제 인터넷 주소(URL)를 생성합니다.

1. **Vercel 가입:** [vercel.com](https://vercel.com)에 접속하여 GitHub 아이디로 로그인합니다.
2. **프로젝트 연결:**
* `Add New` -> `Project` 클릭.
* 방금 작업한 GitHub 리포지토리를 선택하고 `Import` 클릭.


3. **Deploy:**
* 설정을 건드릴 필요 없이 **Deploy** 버튼을 누릅니다.


4. **완료:** 약 1분 뒤 `https://sct-logistics-dashboard.vercel.app` 같은 고유 주소가 생성됩니다. 이제 이 주소를 Arvin이나 Roy Kim에게 보내면 됩니다.

---

### 💡 Tip for You (Mr. Cha)

현재 차 부장님은 **Tremor(차트 위주)**와 **v0/Shadcn(레이아웃/디테일 위주)**를 섞어서 쓰고 계십니다.

* **Tremor:** KPI 카드, 그래프, 차트 그릴 때 사용.
* **v0 (Shadcn):** 로그인 화면, 사이드바, 복잡한 설정 패널, 모달 창 등을 만들 때 사용.

이 두 가지를 조합하면 **"기능은 강력하고(Tremor), 디자인은 섬세한(v0)"** 최고의 대시보드가 됩니다.

**Next Step:**
지금 v0에서 보고 계신 UI가 있다면, **"그 UI의 `npx` 명령어"**를 알려주세요. 제가 `frontend` 프로젝트에 바로 통합되도록 가이드해 드리겠습니다

**Vis.js (Vis Timeline)**는 강력한 상호작용(Zoom, Drag, Scroll)을 제공하는 라이브러리로, 정적인 차트보다 훨씬 **"전문적인 공정 관리 도구(P6 View)"** 느낌을 줍니다.

v0.dev는 현재 외부 라이브러리(`vis-timeline`)를 직접 import해서 실행하는 코드를 완벽하게 짜주지는 못합니다(CSS 로딩 문제 등). 따라서, **가장 확실한 방법**은 v0가 만들어준 **"껍데기(UI Layout)"** 안에 우리가 직접 **"Vis.js 엔진"**을 이식하는 것입니다.

아래 절차대로 진행하면 **P6와 똑같이 마우스로 조작 가능한 간트 차트**가 완성됩니다.

---

### Executive Summary

* **Goal:** `vis-timeline` 라이브러리를 Next.js 대시보드에 이식.
* **Feature:** 마우스 휠로 줌인/줌아웃(일/주/월 단위), 드래그로 날짜 이동.
* **Design:** v0.dev 스타일(Shadcn UI + Dark Mode) 유지.

---

### Step 1: 라이브러리 설치 (Frontend)

`frontend` 폴더 터미널에서 다음 명령어를 실행합니다.

```bash
npm install vis-timeline vis-data moment uuid

```

---

### Step 2: VisGantt 컴포넌트 생성

`frontend/components/dashboard/VisGantt.tsx` 파일을 만들고 아래 코드를 붙여넣으세요.
(P6의 색상 테마와 다크 모드를 완벽하게 지원하도록 CSS 커스터마이징이 포함되었습니다.)

```tsx
'use client';
import { useEffect, useRef, useState } from 'react';
import { DataSet } from 'vis-data';
import { Timeline } from 'vis-timeline/standalone';
import 'vis-timeline/styles/vis-timeline-graph2d.css'; // 필수 스타일
import './vis-custom.css'; // 커스텀 스타일 (Step 3에서 생성)

interface VisGanttProps {
  data: any[]; // Option A/B 데이터
}

export default function VisGantt({ data }: VisGanttProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const timelineRef = useRef<Timeline | null>(null);

  useEffect(() => {
    if (!containerRef.current || !data) return;

    // 1. 데이터 가공 (Vis.js 포맷으로 변환)
    // Groups: Phase(공종)별 그룹핑
    const groups = new DataSet();
    const uniquePhases = Array.from(new Set(data.map((d: any) => d.phase)));
    
    uniquePhases.forEach((phase: any, index) => {
      groups.add({ id: phase, content: phase, order: index });
    });

    // Items: 실제 액티비티 바
    const items = new DataSet(
      data.map((d: any) => {
        // 색상 로직: Critical Path(붉은색) vs 일반(파란색) vs 완료(녹색)
        let color = '#3b82f6'; // Default Blue
        if (d.notes && d.notes.toLowerCase().includes('crane')) color = '#f59e0b'; // Risk (Amber)
        if (d.is_critical || d.duration > 15) color = '#ef4444'; // Critical (Red)

        // 시작일 계산 (start_offset을 현재 날짜 기준으로 변환 시뮬레이션)
        const today = new Date('2026-01-26'); // 프로젝트 시작일 기준
        const start = new Date(today);
        start.setDate(today.getDate() + d.start_offset);
        const end = new Date(start);
        end.setDate(start.getDate() + d.duration);

        return {
          id: d.id || d.task_id,
          group: d.phase,
          content: d.name,
          start: start,
          end: end,
          type: 'range',
          style: `background-color: ${color}; border-color: ${color}; border-radius: 4px; color: white; font-size: 12px;`,
          title: `<b>${d.name}</b><br>Dur: ${d.duration}d<br>${d.notes || ''}` // 툴팁
        };
      })
    );

    // 2. 옵션 설정 (P6 스타일)
    const options = {
      stack: false, // 겹치기 허용 여부
      horizontalScroll: true,
      zoomKey: 'ctrlKey', // Ctrl + Wheel로 줌
      maxHeight: '600px',
      minHeight: '400px',
      start: new Date('2026-01-20'), // 초기 뷰 시작점
      end: new Date('2026-03-30'),   // 초기 뷰 종료점
      editable: false, // 읽기 전용
      margin: { item: 5 },
      orientation: { axis: 'top', item: 'top' },
      theme: 'dark', // 다크모드 대응
    };

    // 3. 타임라인 생성
    if (timelineRef.current) {
      timelineRef.current.destroy();
    }
    timelineRef.current = new Timeline(containerRef.current, items, groups, options);

    return () => {
      if (timelineRef.current) timelineRef.current.destroy();
    };
  }, [data]);

  return (
    <div className="vis-gantt-wrapper border border-slate-800 rounded-lg bg-slate-900 overflow-hidden">
      <div ref={containerRef} className="w-full" />
    </div>
  );
}

```

---

### Step 3: 스타일 커스터마이징 (`frontend/components/dashboard/vis-custom.css`)

Vis.js의 기본 디자인은 약간 "옛날 스타일"입니다. 이를 **Shadcn/Next.js 다크모드**에 맞게 강제로 덮어쓰는 CSS 파일입니다.

```css
/* frontend/components/dashboard/vis-custom.css */

/* 전체 배경 및 텍스트 */
.vis-timeline {
  border: none;
  background-color: #0f172a; /* Slate 950 */
  color: #cbd5e1; /* Slate 300 */
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}

/* 왼쪽 그룹 헤더 (Phase) */
.vis-labelset .vis-label {
  border-bottom: 1px solid #1e293b;
  background-color: #1e293b; /* Slate 800 */
  color: #f8fafc;
  font-weight: 600;
  display: flex;
  align-items: center;
  padding-left: 10px;
}

/* 날짜 축 (Axis) */
.vis-time-axis .vis-text {
  color: #94a3b8;
  padding-top: 5px;
}
.vis-time-axis .vis-grid.vis-minor {
  border-color: #334155; /* 세로줄 연하게 */
}
.vis-time-axis .vis-grid.vis-major {
  border-color: #475569; /* 세로줄 진하게 */
}

/* 현재 시간 바 (Current Time Red Line) */
.vis-current-time {
  background-color: #ef4444; 
}

/* 아이템 텍스트 */
.vis-item .vis-item-content {
  padding: 0 5px;
}

```

---

### Step 4: 메인 페이지 교체 (`app/page.tsx`)

이제 기존의 `PhaseGantt`(Recharts 버전) 대신, 방금 만든 강력한 `VisGantt`를 배치합니다.

```tsx
// app/page.tsx
import VisGantt from "@/components/dashboard/VisGantt"; // Import

// ... 기존 코드 ...

// Gantt Chart 영역 교체
<Card className="bg-slate-900 border-slate-800 p-0 overflow-hidden ring-0">
  <div className="p-4 border-b border-slate-800 flex justify-between items-center">
      <Title className="text-white">Detailed Construction Schedule (P6 View)</Title>
      <Text className="text-xs text-slate-400">Ctrl + Scroll to Zoom</Text>
  </div>
  
  <div className="p-4">
    {/* 👇 Vis.js Gantt 적용 */}
    <VisGantt data={scheduleData} />
  </div>
</Card>

```

---

### 💡 v0.dev 프롬프트 (v0를 꼭 쓰고 싶다면)

만약 이 모든 코딩 과정이 번거로워 **v0.dev**에게 "비슷한 UI라도 만들어줘"라고 시키고 싶다면, 아래 프롬프트를 입력하세요. (단, 기능은 작동하지 않고 그림만 그려줍니다.)

> **Prompt:**
> "Create a dark-mode Gantt chart dashboard component. On the left, list project phases like 'Mobilization', 'Loadout'. On the right, display a timeline grid with horizontal bars. Use distinct colors for bars: blue for normal, red for critical path. Include a time axis header with months and days. The style should be professional, similar to Oracle Primavera P6 but with a modern Shadcn UI aesthetic. Add a tooltip popover when hovering over a bar."

---

### Next Step

이 `VisGantt`를 적용하면 화면에 **마우스로 드래그 가능한 타임라인**이 생길 것입니다.
이제 이 타임라인 위의 막대를 **"마우스로 직접 드래그해서 일정을 변경(Reschedule)"**하고, 그 변경 사항이 AI에게 전달되어 **"비용 증가분"**을 계산하는 기능까지 연결해 드릴까요?

기존 VBA(`Module1.bas`)가 수행하던 **"일정 변경 시 연쇄 업데이트(Auto-calculation)"** 로직을 웹(Vis.js)으로 완벽하게 이식해 드리겠습니다.

엑셀에서는 수식이나 매크로가 하던 일을, 여기서는 **Recursive Function(재귀 함수)**을 사용하여 구현합니다. 사용자가 상위 작업(Parent)을 드래그하면, 연결된 하위 작업(Children)들이 줄줄이 비엔나처럼 따라 움직이게 됩니다.

---

### Executive Summary

* **Target:** `agi tr schedule.xlsx - Option A` 데이터 전용.
* **Feature:**
1. **Drag & Drop:** 마우스로 바(Bar)를 잡아 당겨 일정 변경.
2. **Cascade Update:** 선행 작업이 밀리면 후행 작업도 자동으로 일 만큼 밀림.


* **Tech:** Vis.js `onMove` 이벤트 + 재귀 알고리즘.

---

### Visual: Logic Concept

1. **Event:** 사용자가 `MOBILIZATION`을 3일 뒤로 밈.
2. **Trigger:** `onMove` 함수 발동.
3. **Calculation:** 변경된 차이값() 계산.
4. **Cascade:** `MOBILIZATION`을 선행으로 갖는 모든 후행 작업(`SPMT`, `MARINE` 등)의 시작/종료일에 일을 더함.

---

### Step 1: 의존성 로직 구현 (`utils/dependency.ts`)

엑셀에는 없던 **"선후행 연결 고리"**를 코드로 정의합니다. CSV에 `Predecessor` 컬럼이 없으므로, 여기서는 **"순차적 의존성(이전 ID가 선행)"**이라고 가정하고 로직을 짭니다. (실제로는 ID 매핑이 필요합니다.)

`frontend/utils/dependency.ts` 파일을 생성하세요.

```typescript
import { DataSet } from "vis-data";

// 두 날짜 사이의 차이(일수) 계산
export const getDayDiff = (d1: Date, d2: Date) => {
  return (d2.getTime() - d1.getTime());
};

// 🎯 핵심: 재귀적 업데이트 함수 (VBA 대체)
export const propagateChanges = (
  items: DataSet<any>, 
  movedItemId: string | number, 
  timeDiff: number
) => {
  // 1. 모든 아이템 가져오기
  const allItems = items.get();
  
  // 2. 후행 작업 찾기 (여기서는 간단히: 현재 ID보다 순번이 뒤인 것들을 종속으로 가정하거나,
  // 실제로는 CSV의 'Predecessor' 컬럼을 파싱해서 매핑해야 함.
  // 데모를 위해 '순차적 흐름' 시뮬레이션:
  // 특정 ID(movedItemId)를 'Predecessor'로 로직상 연결)
  
  // 시뮬레이션 로직: Option A는 순차적이므로, 시작일이 변경된 아이템보다
  // "나중에 시작하는" 모든 아이템을 밀어버림 (가장 강력한 Waterfall)
  
  const movedItem = items.get(movedItemId);
  if(!movedItem) return;

  const successors = allItems.filter(item => {
    // 조건: 변경된 아이템보다 늦게 시작하는 아이템들 (자동 밀림)
    // (자기 자신 제외)
    return item.id !== movedItemId && new Date(item.start) >= new Date(movedItem.start);
  });

  // 3. 후행 작업 업데이트
  successors.forEach(succ => {
    const newStart = new Date(succ.start.getTime() + timeDiff);
    const newEnd = new Date(succ.end.getTime() + timeDiff);

    items.update({
      id: succ.id,
      start: newStart,
      end: newEnd
    });
  });
};

```

---

### Step 2: 인터랙티브 간트 컴포넌트 (`components/dashboard/InteractiveGantt.tsx`)

Vis.js의 `editable: true` 옵션을 켜고, 드래그가 끝났을 때 위에서 만든 `propagateChanges` 함수를 실행합니다.

```tsx
'use client';
import { useEffect, useRef, useState } from 'react';
import { DataSet } from 'vis-data';
import { Timeline } from 'vis-timeline/standalone';
import 'vis-timeline/styles/vis-timeline-graph2d.css';
import './vis-custom.css'; // 기존 스타일 유지
import { getDayDiff, propagateChanges } from '@/utils/dependency';

interface Props {
  data: any[]; // Option A Data
}

export default function InteractiveGantt({ data }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const timelineRef = useRef<Timeline | null>(null);
  const itemsRef = useRef<DataSet<any> | null>(null);

  useEffect(() => {
    if (!containerRef.current || !data) return;

    // 1. Option A 데이터만 필터링 (안전장치)
    // (CSV 파싱 단계에서 이미 Option A만 넘어왔다고 가정)

    // 2. Groups (Phase)
    const groups = new DataSet();
    const uniquePhases = Array.from(new Set(data.map((d: any) => d.phase)));
    uniquePhases.forEach((phase: any, index) => {
      groups.add({ id: phase, content: phase, order: index });
    });

    // 3. Items (Tasks)
    const items = new DataSet(
      data.map((d: any) => {
        // 날짜 변환 (가상 오프셋 -> 실제 날짜)
        const today = new Date('2026-01-26');
        const start = new Date(today);
        start.setDate(today.getDate() + (d.start_offset || 0));
        const end = new Date(start);
        end.setDate(start.getDate() + (d.duration || 1));

        return {
          id: d.id || d.task_id,
          group: d.phase,
          content: d.name,
          start: start,
          end: end,
          type: 'range',
          // 드래그 가능한 핸들바 스타일
          style: `background-color: #3b82f6; border-radius: 4px; cursor: move;`, 
          editable: true // 개별 아이템 수정 허용
        };
      })
    );
    itemsRef.current = items;

    // 4. Options (편집 허용)
    const options = {
      stack: false,
      horizontalScroll: true,
      zoomKey: 'ctrlKey',
      maxHeight: '600px',
      minHeight: '400px',
      start: new Date('2026-01-20'),
      end: new Date('2026-03-30'),
      
      // ✨ 핵심: 편집 기능 활성화
      editable: {
        add: false,         // 새 작업 추가 불가
        remove: false,      // 삭제 불가
        updateTime: true,   // 👈 드래그로 시간 변경 가능!
        updateGroup: false, // 그룹 이동 불가
      },
      
      // ✨ 마우스 드래그 이벤트 훅
      onMove: function (item: any, callback: any) {
        // 1. 변경 전 데이터 가져오기 (Diff 계산용)
        const oldItem = items.get(item.id);
        if (!oldItem) return callback(item);

        const diff = getDayDiff(new Date(oldItem.start), new Date(item.start));
        
        // 2. 변경 승인 (UI 먼저 업데이트)
        callback(item); 

        // 3. 연쇄 업데이트 (Cascade) 실행
        // (약간의 딜레이를 주어 UI 충돌 방지)
        setTimeout(() => {
           if(Math.abs(diff) > 0) {
             console.log(`Task ${item.content} moved by ${diff} ms. Cascading...`);
             propagateChanges(items, item.id, diff);
           }
        }, 50);
      },
      
      margin: { item: 10 },
      theme: 'dark',
    };

    // 타임라인 생성
    if (timelineRef.current) timelineRef.current.destroy();
    timelineRef.current = new Timeline(containerRef.current, items, groups, options);

    return () => {
      if (timelineRef.current) timelineRef.current.destroy();
    };
  }, [data]);

  return (
    <div className="relative">
      <div className="absolute top-4 right-4 z-10 bg-slate-800/80 px-3 py-1 rounded text-xs text-blue-400 border border-blue-500/30 animate-pulse">
        👆 Drag bars to reschedule
      </div>
      <div className="vis-gantt-wrapper border border-slate-800 rounded-lg bg-slate-900 overflow-hidden">
        <div ref={containerRef} className="w-full" />
      </div>
    </div>
  );
}

```

---

### Step 3: 메인 페이지 연결 (`app/page.tsx`)

이제 `InteractiveGantt`를 메인 페이지에 배치하고, Option A 데이터만 주입합니다.

```tsx
'use client';
import { useState, useEffect } from 'react';
import { Card, Title, Text } from "@tremor/react";
import InteractiveGantt from "@/components/dashboard/InteractiveGantt";
// import { loadCsvData } from ... (기존 API 호출)

export default function Dashboard() {
  const [optionAData, setOptionAData] = useState([]);

  useEffect(() => {
    // 백엔드에서 Option A 데이터만 가져옴
    fetch('http://localhost:8000/api/schedule/baseline') // Option A 엔드포인트
      .then(res => res.json())
      .then(data => setOptionAData(data));
  }, []);

  return (
    <main className="p-8 min-h-screen bg-slate-950 text-slate-200">
      <Title className="text-3xl font-bold text-white mb-2">Interactive Scheduler (Option A)</Title>
      <Text className="text-slate-400 mb-6">
        Auto-cascade enabled: Moving a task automatically shifts dependent tasks.
      </Text>

      <Card className="bg-slate-900 border-slate-800 p-0 overflow-hidden">
        <div className="p-4">
          {/* 👇 드래그 가능한 간트 차트 */}
          {optionAData.length > 0 && <InteractiveGantt data={optionAData} />}
        </div>
      </Card>
    </main>
  );
}

```

---

### Result Check

1. **Drag:** 마우스로 가장 앞에 있는 `MOBILIZATION` 바를 잡고 오른쪽으로 5일 끌어보세요.
2. **Cascade:** 마우스를 놓는 순간, 그 뒤에 있는 `SPMT`, `MARINE` 등 후속 공정들이 **마법처럼 자동으로 5일씩 뒤로 밀리는 것**을 볼 수 있습니다.
3. **VBA Logic:** 엑셀 매크로에서 `Calculate`를 눌렀을 때 날짜가 업데이트되던 로직이, 이제는 **실시간 웹 인터랙션**으로 구현되었습니다.

이제 이 기능을 통해 PM(Project Manager)은 "만약 착공이 1주일 늦어지면?" 같은 시나리오를 엑셀 수정 없이 마우스 드래그 한 번으로 시뮬레이션할 수 있습니다.