# Student Admission ERP Platform

A production-ready **Student Registration and Admission Management** platform built with **Odoo 17** (backend) and **Next.js 14** (web portal deployable on Vercel).

## Architecture

```
┌─────────────────────┐     REST API      ┌──────────────────────┐
│   Next.js Portal    │ ◄──────────────► │   Odoo 17 Backend    │
│   (Vercel)          │   /api/v1/*       │   (Docker/Cloud)     │
│   student-portal/   │                   │   student_admission/ │
└─────────────────────┘                   └──────────┬───────────┘
                                                       │
                                            ┌──────────▼───────────┐
                                            │   PostgreSQL 15      │
                                            └──────────────────────┘
```

## Project Structure

```
├── student_admission/     # Odoo 17 ERP module
├── student-portal/        # Next.js 14 web portal (Vercel)
├── deployment/            # Docker Compose + scripts
├── docs/student-admission/  # Guides & API docs
└── .github/workflows/     # CI/CD pipelines
```

## Quick Start

```bash
# 1. Start Odoo + PostgreSQL (auto-creates DB + installs modules)
chmod +x deployment/start.sh && ./deployment/start.sh

# 2. Start Next.js portal
chmod +x deployment/start-portal.sh && ./deployment/start-portal.sh

# OR start all services with Docker:
cp deployment/.env.example .env
docker compose -f deployment/docker-compose.yml up -d
```

- **Portal:** http://localhost:3000
- **Odoo:** http://localhost:8069 (admin / admin)
- **Health:** http://localhost:8069/api/health · http://localhost:3000/api/health

See **[docs/student-admission/RUNNING_GUIDE.md](docs/student-admission/RUNNING_GUIDE.md)** for full instructions.

## Features

| Module | Backend | Portal |
|--------|---------|--------|
| Student Registration | ✅ | ✅ Online form |
| Admission Workflow | ✅ 7 states | ✅ Status tracker |
| Academic Structure | ✅ | ✅ Course listing |
| Fee Management | ✅ Scholarships/discounts | ✅ Fee status |
| Document Verification | ✅ | ✅ Upload & track |
| Dashboard KPIs | ✅ | ✅ Student dashboard |
| Role-Based Security | ✅ 7 roles | ✅ Auth |
| Reports | ✅ 7 reports | — |
| REST API | ✅ v1 | ✅ Client |
| Email Notifications | ✅ | — |
| Dark/Light Mode | — | ✅ |

## Deployment

| Component | Platform | Guide |
|-----------|----------|-------|
| Frontend | **Vercel** | [VERCEL_DEPLOYMENT.md](docs/student-admission/VERCEL_DEPLOYMENT.md) |
| Backend | Docker / Railway / AWS | [DOCKER_DEPLOYMENT.md](docs/student-admission/DOCKER_DEPLOYMENT.md) |
| API Reference | — | [API.md](docs/student-admission/API.md) |
| Testing | — | [TESTING.md](docs/student-admission/TESTING.md) |
| Local Dev | — | [LOCAL_DEVELOPMENT.md](docs/student-admission/LOCAL_DEVELOPMENT.md) |

## Step-by-Step Deployment

### 1. Run Locally
See [LOCAL_DEVELOPMENT.md](docs/student-admission/LOCAL_DEVELOPMENT.md)

### 2. Run with Docker
```bash
cd deployment && docker compose up -d --build
```

### 3. Deploy Frontend to Vercel
```bash
cd student-portal && npx vercel
```
Set `NEXT_PUBLIC_ODOO_URL` to your Odoo backend URL.

### 4. Deploy Odoo Backend
Use `deployment/Dockerfile.odoo` on Railway, Render, AWS EC2, or Azure.

### 5. Connect Vercel ↔ Odoo
1. Set `NEXT_PUBLIC_ODOO_URL` in Vercel env vars
2. Set `STUDENT_ADMISSION_CORS_ORIGINS` on Odoo to your Vercel URL
3. Redeploy both services

### 6. Verify
```bash
curl https://your-odoo.railway.app/api/v1/courses
open https://your-app.vercel.app/courses
```

## Demo Users

| Role | Email | Password |
|------|-------|----------|
| Admin | admin | admin |
| Admission Officer | admission.officer@institute.edu | demo123 |
| Account Officer | accounts@institute.edu | demo123 |
| Student | rahul.sharma@example.com | demo123 |

## License

LGPL-3
