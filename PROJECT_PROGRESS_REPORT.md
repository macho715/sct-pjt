# ADNOC HVDC Scheduler AI - Project Progress Report

**Date:** 2026-01-17
**Version:** 2.1 (Interactive Update)

## 1. Executive Summary
This report details the development progress of the **ADNOC HVDC Scheduler AI** system. The project has evolved from a basic data viewer into an interactive, AI-assisted project management tool. Key achievements include the successful integration of complex Excel data, the implementation of a hierarchical dashboard, and the deployment of a P6-style interactive Gantt chart with auto-cascading logic.

## 2. Development Phases & Milestones

### Phase 1: Foundation & Data Integration
*   **Repository Setup**: Initialized Git repository and synchronized with GitHub (`macho715/sct-pjt`).
*   **Architecture Design**: Established a Client-Server architecture using Next.js 14 (Frontend) and FastAPI (Backend).
*   **Data Pipeline**:
    *   Analyzed raw Excel inputs (`agi tr schedule.xlsx`).
    *   Developed scripts to convert Excel sheets (`Schedule_Data_Option_A`, `B`) into JSON-compatible CSVs.
    *   **Logic Correction**: Diagnosed and fixed duration calculation discrepancies (Baseline: 43 days vs Optimized: 66 days) by implementing precise date-range logic instead of simple summation.

### Phase 2: User Experience (UX) Overhaul
*   **Hydration Error Fix**: Resolved Next.js server-client mismatch issues in `layout.tsx`.
*   **Hierarchical Gantt View**:
    *   Implemented `PhaseGantt` component using Tremor Accordions.
    *   Grouped 100+ tasks by "Phase" (e.g., MOBILIZATION, INSTALLATION) to reduce cognitive load.
    *   Added Sticky Headers for better timeline navigation.
*   **Task Details Drawer**:
    *   Created `TaskDrawer` component for deep-dive analysis.
    *   Integrated a mock "AI Risk Analyst" that evaluates task notes for potential risks (High/Low).

### Phase 3: Interactive Scheduler (Patch 1 Implementation)
*   **Library Integration**: Installed `vis-timeline` and `vis-data` for advanced visualization.
*   **Component Development**:
    *   **InteractiveGantt**: A drag-and-drop enabled Gantt chart replicating Oracle Primavera P6 functionality.
    *   **Custom Styling**: Developed `vis-custom.css` to match the dashboard's "Slate" dark mode theme.
*   **Logic Engine**:
    *   **Auto-Cascade (`dependency.ts`)**: Implemented recursive logic (`propagateChanges`) that automatically updates successor task dates when a predecessor is moved.
*   **View Switching**: Updated the main dashboard to allow users to toggle between the "Hierarchical View" (Overview) and "Interactive View" (Edit Mode).

### Phase 3.5: Backend Persistence & Stability (Completed)
*   **Backend Synchronization**:
    *   **Endpoint**: Implemented `POST /api/schedule/save` in `backend/main_api.py`.
    *   **Functionality**: Saves modified `vis-timeline` data back to the server CSVs.
    *   **Safety**: Automatically creates timestamped backups in `backend/data/history/` before overwriting.
    *   **UI Integration**: Added a "Save Changes to Server" button in `InteractiveGantt.tsx` that triggers the sync.
*   **Critical Bug Fixes**:
    *   **Hydration Error**: Fixed server/client mismatch by adding `suppressHydrationWarning` to `layout.tsx`.
    *   **Duplicate ID Crash**: Implemented deduplication logic in `InteractiveGantt.tsx` to handle unclean input data safely.
    *   **Timeline Cleanup Error**: Added `try-catch` blocks around `vis-timeline` destruction to prevent "null property" runtime crashes during re-renders.
*   **Maintenance**:
    *   **Dependency Upgrade**: Started upgrade process for Next.js (v16.1.2) to resolve version staleness warnings.

## 3. Technical Deliverables

### A. Documentation
| Document | Description |
| :--- | :--- |
| `README.md` | Project overview, installation guide, and feature list. |
| `SYSTEM_ARCHITECTURE.md` | High-level system design, class diagrams, and stack details. |
| `DASHBOARD_STRUCTURE.md` | Visual breakdown of UI components and interaction flows. |
| `PROJECT_PROGRESS_REPORT.md` | Detailed log of development phases and changelog. |

### B. Key Source Code
1.  **Frontend**:
    *   `app/page.tsx`: Main dashboard controller with View Mode toggle.
    *   `components/dashboard/PhaseGantt.tsx`: Accordion-based read-only view.
    *   `components/dashboard/InteractiveGantt.tsx`: Editable P6-style view with Save Logic.
    *   `components/ui/TaskDrawer.tsx`: Slide-out details panel.
    *   `utils/dependency.ts`: Core logic for date propagation.
2.  **Backend**:
    *   `main_api.py`: FastAPI server with Save/Backup endpoints.
    *   `scripts/`: Python utilities for data processing.

### Phase 4: Dynamic Cost Engine (Completed)
*   **Cost Calculation**:
    *   **Backend**: Injected `daily_rate` and `total_cost` calculation into `main_api.py`.
    *   **Frontend**: Implemented real-time cost tracking in `InteractiveGantt.tsx`. Dragging a task now instantly updates the specific task cost and the global "Total Project Cost" KPI.

### Phase 5: P6-Style Visual Enhancements (Completed)
*   **Visual Standard**: Upgraded Gantt visual language to match **Oracle Primavera P6**.
    *   **Milestones**: Rendered as distinct diamond shapes (◆).
    *   **Critical Path**: Highlighted critical red bars for tasks > 30 days or marked 'critical'.
    *   **Buffers**: Striped patterns for buffer/waiting tasks.
    *   **UI Tuning**: Removed excessive grid lines, added current-time markers, and refined tooltips.

### Phase 6: Voyage-Centric Restructuring (Completed)
*   **Grouping Logic**: Shifted from generic "Phase" grouping to **Voyage/Shipment** based grouping (e.g., "Voyage 1 (TR Units 1 & 2)").
*   **Implementation**:
    *   Created `utils/voyageLogic.ts` for centralized grouping rules.
    *   Updated `InteractiveGantt` to group tasks by Voyage ID ranges, aligning with logistics operations.

### Phase 7: Ontology-Driven Insights (In Progress)
*   **Voyage Risk Profile (Implemented)**:
    *   **Logic**: Developed `riskLogic.ts` based on `CONSOLIDATED-04` ontology.
    *   **Features**: Automatically flags "Heavy Lift" (>40t), "Tandem Lifts", and "Sensitive Cargo" (Cable).
    *   **UI**: Adds Risk Borders (Red/Orange) and Icons (🔥/⚠️) to Gantt bars.
*   **Advanced Compliance (Planned)**:
    *   **Flow Code v3.5**: Visualizing logic flow (0-5) and efficiency.
    *   **AGI/DAS Rules**: Enforcing mandatory MOSB legs for offshore sites.

## 4. Current Status
The system has evolved into a **Logistics-Aware Project Intelligence Tool**.
1.  **Risk-Aware**: It sees beyond dates—identifying risks in cargo types and voyage complexity.
2.  **Cost-Dynamic**: Scheduler changes reflect financial impact immediately.
3.  **Operationally Aligned**: Grouping by Voyage matches the actual execution model.

## 5. Next Steps
*   **Phase 7B**: Implement Flow Code & AGI/DAS Compliance Rules.
*   **Phase 7C**: Implement Cost Guard (Budget Traffic Lights).
*   **Deployment**: Finalize git sync and prepare for deployment.

