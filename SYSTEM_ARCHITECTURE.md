# System Architecture

## 1. High-Level Overview

The system follows a modern client-server architecture, designed to process logistics data and visualize it through an interactive dashboard.

```mermaid
graph TD
    User((User)) -->|Access via Browser| Client[Frontend Client]
    Client -->|REST API Requests| Server[Backend Server]
    
    subgraph "Server Side"
        Server -->|Executes| Scripts[Python Analytical Scripts]
        Server -->|Reads/Writes| Data[(Data Files - Excel/CSV)]
    end
    
    subgraph "Client Side"
        Client -->|Renders| Dashboard[Interactive Dashboard]
    end
```

## 2. Component Architecture

The application is divided into a **Next.js Frontend** for the user interface and a **FastAPI Backend** for data processing and logic execution.

### Frontend (`/frontend`)
- **Technology**: Next.js 14, React, TypeScript
- **State Management**: React Hooks & Context
- **UI Library**: Tremor (Charts), Headless UI, Tailwind CSS

### Backend (`/backend`)
- **Technology**: Python, FastAPI, Uvicorn
- **Core Responsibilities**:
    - **API Layer**: Exposes endpoints for the frontend.
    - **Data Processing**: Uses `pandas` and `openpyxl` to manipulate Excel data.
    - **Script Execution**: Triggers standalone Python scripts in the `/scripts` directory.

```mermaid
classDiagram
    class Frontend {
        +Pages (Next.js)
        +Components (Tremor)
        +Services (API Client)
    }
    
    class Backend {
        +MainAPI (FastAPI)
        +Routers
        +DataGeneration
    }
    
    class DataLayer {
        +Excel Files
        +CSV Files
    }

    Frontend --> Backend : HTTP Requests
    Backend --> DataLayer : File I/O
```

## 3. Data Processing Pipeline

The core value of the system is the transformation of raw logistics data into actionable insights.

```mermaid
sequenceDiagram
    autonumber
    participant Source as Data Source (Excel)
    participant Script as Python Scripts
    participant API as Backend API
    participant UI as Frontend Dashboard

    Note over Source, Script: Data Ingestion
    Source->>Script: Read Raw Shipment Data
    
    Note over Script, API: Processing
    Script->>Script: Validate & Calculate Costs
    Script->>API: Return Processed JSON
    
    Note over API, UI: Visualization
    API->>UI: Send Data Response
    UI->>UI: Render Gantt Charts & Tables
```

## 4. Folder Structure & Responsibilities

| Directory | Responsibility | Key Files |
|-----------|----------------|-----------|
| `frontend/` | Web Interface | `app/`, `components/`, `lib/` |
| `backend/` | API Server | `main_api.py`, `routers/` |
| `scripts/` | Business Logic | `check_invoice.py`, `check_cargo.py` |
| `data/` | Data Storage | `*.xlsx`, `*.csv` |
