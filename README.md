# Mini SaaS Tracker

A modern, full-stack issue and insights tracker for SaaS teams. Built with FastAPI, SvelteKit, PostgreSQL, Docker, and robust RBAC.

---

## 🚀 Features
- **Authentication & RBAC:** JWT-based OAuth2, roles: ADMIN, MAINTAINER, REPORTER
- **Issue Tracking:** Title, description (Markdown), file upload, severity, priority, tags, status workflow
- **Strict Status Workflow:** OPEN → TRIAGED → IN_PROGRESS → DONE
- **Real-time Updates:** WebSocket-powered auto-refresh for issue lists
- **Dashboard & Analytics:** Colorful charts, recent issues, trends, and summary
- **Background Jobs:** APScheduler worker aggregates daily stats
- **Observability:** Structured logging, Prometheus metrics
- **API Docs:** OpenAPI/Swagger at `/api/docs`
- **CI/CD:** GitHub Actions for lint, test, Docker build, migrations
- **Containerized:** Docker Compose for web, db, worker, nginx

---

## 🛠️ Tech Stack & Key Choices
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL, APScheduler, Prometheus
- **Frontend:** SvelteKit, TailwindCSS, custom SVG charts
- **Auth:** JWT-based OAuth2 (see [ADR-001](docs/adr-001-jwt-auth-rbac.md))
- **RBAC:** Enforced in both backend (route dependencies) and frontend (UI logic)
- **Testing:** Pytest (backend), Playwright (E2E, recommended)
- **CI/CD:** GitHub Actions
- **Containerization:** Docker, docker-compose

---

## ⚡ Quick Start

### 1. Clone & Setup
```bash
# Clone repo
 git clone https://github.com/nevilsonani/issues-insights-tracker.git
 cd mini-saas-tracker

# Copy .env files as needed (see .env.example)
```

### 2. Run with Docker Compose
```bash
docker-compose up --build
```
- Frontend: http://localhost:3000
- Backend/API: http://localhost:8000
- Swagger docs: http://localhost:8000/api/docs
- Prometheus metrics: http://localhost:8000/metrics

### 3. Run Tests & Coverage
```bash
# Backend
cd backend
pytest --cov=app --cov-report=term-missing

# Frontend (optional)
cd ../frontend
npm install
npm run test
```

---

## 🧩 Project Structure
```
mini-saas-tracker/
  backend/      # FastAPI app, DB, workers
  frontend/     # SvelteKit app
  worker/       # Background job Docker image
  tests/        # Backend tests
  .github/      # GitHub Actions workflows
  docs/         # Architecture Decision Records (ADR)
```

---

## 🌟 Future Improvements
- S3/GCS file upload support
- Advanced analytics & filtering
- More granular permissions (per-project, per-tag)
- OAuth2 PKCE or session cookie auth
- User profile & notifications
- Export/import (CSV, JSON)
- More E2E tests (Playwright/Cypress)
- Dark mode & theme customization
- Multi-language support

---

## 📚 References
- [ADR-001: JWT-based OAuth2 for Auth & RBAC](docs/adr-001-jwt-auth-rbac.md)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SvelteKit Docs](https://kit.svelte.dev/)
- [Prometheus Python Client](https://github.com/prometheus/client_python)

