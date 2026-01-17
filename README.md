# Event Management System

A robust, enterprise-grade event management application built with **FastAPI** (Python) and **Angular** (TypeScript), following the **Hexagonal Architecture** (Clean Architecture) pattern.

## 🚀 Overview

This project provides a comprehensive platform for managing events, users, and attendance records. It emphasizes clean separation of concerns, testability, and scalability.

## 🏗️ Architecture

Both backend and frontend follow the **Hexagonal Architecture**:

- **Domain**: Pure business entities and logic.
- **Application**: Use cases and Ports (Interfaces) orchestrating operations.
- **Infrastructure**: Adapters for database (SQLAlchemy), parsers (CSV), and API clients.
- **Presentation**: Web routers/schemas (FastAPI) and Components (Angular).

See [ADR.md](./ADR.md) for detailed architectural decisions.

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLAlchemy 2.0, Pydantic V2, PostgreSQL (via SQLite in dev), Alembic.
- **Frontend**: Angular 18+, Signals for state management, Vanilla CSS/HSL design system.
- **Testing**: Pytest (Backend), Karma/Jasmine (Frontend).

## 🚦 Quick Start

### Automated Setup (Windows)
Run the following script to set up environments and start both backend and frontend:
```powershell
.\run.ps1
```

### Manual Setup

#### Backend
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```powershell
cd frontend
npm install
npm run dev
```

## 🧪 Testing
See the [Walkthrough](./brain/9b59402a-4529-4a0a-b672-0ee113698c28/walkthrough.md) for details on running tests and verification steps.
