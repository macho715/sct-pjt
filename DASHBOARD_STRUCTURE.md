# Dashboard Screen Composition & Architecture

This document outlines the visual structure and component hierarchy of the **ADNOC HVDC Scheduler AI** dashboard. It provides a graphical representation of the user interface layout and the flow of interactions.

## 1. High-Level Screen Layout

The dashboard follows a **Single Page Application (SPA)** layout with a persistent header, a KPI summary grid, and a central workspace for the schedule visualization, augmented by an interactive details drawer.

```mermaid
graph TD
    Root[App Container]
    
    subgraph "Global Header"
        Header[Utility Bar] --> Logo[Title & Version]
        Header --> Actions[Global Actions]
        Actions --> RiskBtn[Bulk Risk Scan Button]
        Actions --> Badge[AI Accuracy Badge]
    end

    subgraph "KPI Section (Grid Layout)"
        KPIs[KPI Grid]
        KPIs --> Card1[Total Duration Widget]
        KPIs --> Card2[Recovered Days Widget]
        KPIs --> Card3[Est. Budget Widget]
        KPIs --> Control[Simulation Control Button]
    end

    subgraph "Main Content Area"
        Main[PhaseGantt Container]
        Main --> G_Header[Chart Header & Active Scenario Legend]
        Main --> AccordionList[Phase Accordion List]
        
        AccordionList --> Phase1[Phase: MOBILIZATION]
        AccordionList --> Phase2[Phase: TRANSPORT]
        AccordionList --> Phase3[Phase: INSTALLATION]
        
        Phase1 --> BarChart1[Gantt Bars]
        Phase2 --> BarChart2[Gantt Bars]
    end

    subgraph "Interactive Overlays"
        Drawer[Task Details Drawer]
        RiskModal[Risk Analysis Modal]
    end

    Root --> Header
    Root --> KPIs
    Root --> Main
    Root -.-> Drawer
    Root -.-> RiskModal
    
    BarChart1 -.->|Click Task| Drawer
    Control -.->|Click Run| Main
```

## 2. Component Detail Specification

### 2.1 Header Area
*   **Purpose**: Branding and global utilities.
*   **Elements**:
    - **Project Title**: "ADNOC HVDC Scheduler AI"
    - **Sub-text**: "Anti-Gravity Engine v2.0 Active"
    - **Risk Scan**: Triggers project-wide risk assessment algorithm (showing 🔥/⚠️).
    - **AI Badge**: Displays confidence score (e.g., "AI Accuracy 94%").
    - **View Tabs**: "Hierarchical (Read-Only)" vs "Interactive (P6 Style)".

### 2.2 KPI & Control Grid
*   **Purpose**: High-level metrics and scenario switching.
*   **Layout**: 4-Column Grid.
*   **Components**:
    1.  **Total Duration**: Shows project length (Dynamic: Option A vs B).
    2.  **Recovered Days**: Calculates time saved (`Baseline - Optimized`). Highlights positive impact in green.
    3.  **Est. Budget**: Financial summary.
    4.  **Control Button**: Interactive button to "Run Anti-Gravity" (Switch to Option B) or "Reset" (Back to Option A).

### 2.3 Hierarchical Gantt Chart (`PhaseGantt`)
*   **Purpose**: Visualization of the project timeline managed by Phases.
*   **Interaction**: Accordion style (Expand/Collapse).
*   **Structure**:
    *   **Sticky Header**: Shows timeline range (Days) and persists on scroll.
    *   **Accordion Items**: grouped by `Phase`.
    *   **Gantt Rows**: Each row represents a task.
        *   **Left**: Task Name.
        *   **Bar**: Visual length proportional to duration. Color-coded by Phase.

### 2.4 Task Detail Drawer (`TaskDrawer`)
*   **Purpose**: Deep-dive analysis for a selected task without leaving the main view.
*   **Trigger**: Clicking any Gantt bar.
*   **Content**:
    *   **Header**: Task Name, ID, Phase Badge.
    *   **Metrics**: Duration, Owner.
    *   **Notes**: Raw log data or constraints.
    *   **AI Analyst**:
        *   **Button**: "Ask AI Assistant"
        *   **Result**: Risk Level (High/Low), text analysis, and actionable recommendation.

### 2.5 Interactive Gantt (`InteractiveGantt`)
*   **Purpose**: Editable, professional scheduling view (Primavera P6 replacement).
*   **Visuals**:
    *   **Milestones**: Diamond shapes (◆).
    *   **Risks**: Left-border color codes (Red=Critical, Orange=High) + Icons.
    *   **Grouping**: Grouped by **Voyage/Shipment** instead of generic phases.
*   **Features**:
    *   **Drag & Drop**: Moving a task auto-updates dependent tasks.
    *   **Save Button**: Persists changes to backend CSVs.

## 3. Interaction Flow Logic


```mermaid
sequenceDiagram
    participant User
    participant KPI as KPI Grid
    participant Chart as PhaseGantt
    participant Drawer as TaskDrawer
    participant AI as AI Engine

    User->>KPI: Click "Run Anti-Gravity"
    KPI->>KPI: Show Loading State
    KPI->>Chart: Switch Data Source (Option B)
    KPI->>KPI: Update Metric (Recovered Days)
    
    User->>Chart: Expand "MOBILIZATION" Phase
    Chart->>Chart: Reveal Task Bars for Phase
    
    User->>Chart: Click Task "MOB-001"
    Chart->>Drawer: Open Drawer (Slide-in)
    
    User->>Drawer: Click "Ask AI Assistant"
    Drawer->>AI: Request Risk Analysis (Task Data)
    AI-->>Drawer: Return Risk Level & Advice
    Drawer->>User: Display AI Insight
```
