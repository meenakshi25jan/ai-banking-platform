# Repository Split — Student Admission ERP

This document maps the **ai-banking-platform** monorepo split into two standalone repositories.

## Split repositories (ready to push)

| Repository | Directory | Purpose |
|------------|-----------|---------|
| **student-admission-odoo-backend** | `/student-admission-odoo-backend/` | Odoo 17 + PostgreSQL + Docker |
| **student-admission-portal-vercel** | `/student-admission-portal-vercel/` | Next.js portal for Vercel |

> Original code in `student_admission/`, `student-portal/`, and `deployment/` is **preserved** in this monorepo.

---

## TASK 1: Analysis — Backend files (Odoo)

### Odoo custom module
```
student_admission/
├── __init__.py, __manifest__.py, README.md
├── models/          (14 Python files)
├── controllers/     (api_v1.py, cors.py, main.py)
├── views/           (14 XML files)
├── security/        (security.xml, ir.model.access.csv)
├── data/            (sequences, mail templates, cron)
├── demo/            (demo_data.xml, demo_users.xml)
├── wizard/          (reject wizards)
├── report/          (QWeb PDF reports)
├── tests/           (unit + integration tests)
└── static/description/
```

### Deployment & Docker (backend)
```
deployment/
├── Dockerfile.odoo → moved to deployment/Dockerfile in backend repo
├── entrypoint-odoo.sh → deployment/entrypoint.sh
├── odoo.conf
├── start.sh, stop.sh
├── lib/common.sh
└── .env.example → root .env.example in backend repo

docker-compose.yml (root) — Odoo + PostgreSQL only in backend repo
```

### Backend docs
```
docs/student-admission/
├── API.md
├── DOCKER_DEPLOYMENT.md
├── LOCAL_DEVELOPMENT.md
├── RUNNING_GUIDE.md
├── TESTING.md
└── READINESS_REPORT.md
```

### Backend CI
```
.github/workflows/student-admission-odoo.yml
```

**Total backend files:** ~68

---

## TASK 1: Analysis — Frontend files (Vercel)

```
student-portal/
├── src/app/         (pages + api/health)
├── src/components/  (Navbar, Footer, Theme)
├── src/lib/         (api.ts, auth.tsx)
├── public/
├── package.json, package-lock.json
├── next.config.js, tsconfig.json, tailwind.config.ts
├── vercel.json
├── .env.example
└── deploy-vercel.sh
```

### Frontend CI
```
.github/workflows/student-admission-portal.yml
```

**Total frontend files:** ~35

---

## TASK 1: Analysis — Keep in ai-banking-platform

These are **NOT** part of Student Admission ERP:

| Path | Product |
|------|---------|
| `ai-service/` | Banking AI service |
| `client/` | Banking React frontend |
| `server/` | Banking Node.js API |
| `sentinel-ai-complete/` | Sentinel AI governance |
| `infrastructure/` | AWS CloudFormation |
| `docker-compose.yml` (root) | Banking stack |
| `docs/` (except student-admission) | Banking docs |
| `.github/workflows/deploy.yml` | Banking CI |

### Monorepo files to remove after split (optional, later)

| Path | Action |
|------|--------|
| `student_admission/` | Keep until backend repo verified, then remove |
| `student-portal/` | Keep until portal repo verified, then remove |
| `deployment/` | Keep until backend repo verified, then remove |
| `vercel.json` (root) | Remove — caused Vercel 404 |
| `STUDENT_ADMISSION_README.md` | Replace with pointer to split repos |
| `docs/student-admission/` | Move to backend repo only |

---

## Why Vercel was failing

1. **Mixed monorepo** — Vercel detected Python/Docker/Odoo files alongside Next.js
2. **Root `vercel.json`** — Pointed at subdirectory with legacy builder
3. **`output: 'standalone'`** — Docker-only setting incompatible with Vercel
4. **No Root Directory** — Git deploy used repo root instead of `student-portal/`

**Fix:** Deploy `student-admission-portal-vercel` as its own Vercel project.

---

## Push to GitHub as separate repos

```bash
# 1. Create repos on GitHub:
#    - student-admission-odoo-backend
#    - student-admission-portal-vercel

# 2. Push backend
cd student-admission-odoo-backend
git init
git add .
git commit -m "Initial commit: Odoo 17 Student Admission ERP backend"
git remote add origin git@github.com:YOUR_ORG/student-admission-odoo-backend.git
git branch -M main
git push -u origin main

# 3. Push portal
cd ../student-admission-portal-vercel
git init
git add .
git commit -m "Initial commit: Next.js Student Admission portal"
git remote add origin git@github.com:YOUR_ORG/student-admission-portal-vercel.git
git branch -M main
git push -u origin main

# 4. Connect Vercel to student-admission-portal-vercel only
```

---

## Environment variable contract

| Variable | Set on | Value |
|----------|--------|-------|
| `NEXT_PUBLIC_ODOO_URL` | Vercel (portal) | `https://your-odoo-host.com` |
| `NEXT_PUBLIC_ODOO_DB` | Vercel (portal) | `student_admission` |
| `STUDENT_ADMISSION_CORS_ORIGINS` | Odoo (backend) | `https://your-app.vercel.app` |
