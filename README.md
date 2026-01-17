# Project Scheduler AI - ADNOC HVDC

**Anti-Gravity Engine v2.0 - Native Mode**

## Overview
This project is an AI-driven logistics and scheduling dashboard designed for ADNOC HVDC. It provides a comprehensive view of shipment status, financial summaries, and project timelines using a modern web interface and a robust backend.

## System Architecture

### Frontend (`/frontend`)
- **Framework**: Next.js 14 (App Router)
- **UI Components**: Tremor (Charts/Dashboards), Headless UI
- **Styling**: Tailwind CSS, Framer Motion
- **Language**: TypeScript

### Backend (`/backend`)
- **Framework**: FastAPI (Python)
- **Server**: Uvicorn
- **Environment**: Python Virtual Environment (`venv`)

### Data & Scripts
- **Data Source**: Excel / CSV integration (`*.xlsx`, `*.csv`)
- **Scripts**: Python automation scripts for data processing and scenario analysis.

## Prerequisites
- **Node.js**: (Latest LTS recommended)
- **Python**: 3.8+
- **Git**

## Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/macho715/sct-pjt.git
    cd sct-pjt
    ```

2.  **Frontend Setup**
    ```bash
    cd frontend
    npm install
    cd ..
    ```

3.  **Backend Setup**
    ```bash
    cd backend
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    # source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    ```

## Usage

### Windows (Automated)
Simply run the included batch file to start both the backend and frontend servers automatically:
```cmd
Start_System.bat
```
This script will:
1.  Launch the FastAPI backend on port **8000**.
2.  Launch the Next.js frontend on port **3000**.
3.  Open the dashboard in your default browser.

### Manual Start

**Backend**
```bash
cd backend
venv\Scripts\activate
uvicorn main_api:app --reload --port 8000
```

**Frontend**
```bash
cd frontend
npm run dev
```

## Directory Structure
```
sct-pjt/
├── frontend/       # Next.js Web Application
├── backend/        # FastAPI Server
├── data/           # Data files and resources
├── scripts/        # Utility scripts
├── skills/         # Agent skills and logic
├── Start_System.bat # Windows Launcher
└── README.md       # Project Documentation
```
