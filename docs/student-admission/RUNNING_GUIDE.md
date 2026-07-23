# Student Admission ERP — Running Guide

Complete instructions to run the platform locally and deploy to production.

---

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Docker | 24+ with Compose v2 | Odoo + PostgreSQL (+ optional portal) |
| Node.js | 18+ | Local portal development |
| npm | 9+ | Portal dependencies |
| curl | any | Health-check verification |

---

## Run Locally (Recommended)

### Step 1 — Start Odoo Backend

```bash
chmod +x deployment/start.sh
./deployment/start.sh
```

This script will:
1. Verify Docker is installed
2. Create `.env` from `deployment/.env.example` if missing
3. Build and start **PostgreSQL** (port 5433) and **Odoo** (port 8069)
4. Create database `student_admission` on first run
5. Install `base` and `student_admission` modules with demo data
6. Wait until `http://localhost:8069/api/health` returns OK

**First run takes 3–5 minutes** while Odoo initializes the database.

### Step 2 — Start Next.js Portal

```bash
chmod +x deployment/start-portal.sh
./deployment/start-portal.sh
```

This script will:
1. Start Odoo automatically if it is not already running
2. Create `student-portal/.env.local` from `.env.example` if missing
3. Run `npm install`
4. Start Next.js dev server on **port 3000**
5. Verify `http://localhost:3000/api/health`

### URLs

| Service | URL |
|---------|-----|
| **Portal** | http://localhost:3000 |
| **Odoo** | http://localhost:8069 |
| Portal health | http://localhost:3000/api/health |
| Odoo health | http://localhost:8069/api/health |
| Odoo API | http://localhost:8069/api/v1/courses |

### Default Credentials

| Role | Login | Password |
|------|-------|----------|
| Odoo Admin | admin | admin |
| Admission Officer | admission.officer@institute.edu | demo123 |
| Account Officer | accounts@institute.edu | demo123 |
| Student | rahul.sharma@example.com | demo123 |

---

## Run with Docker (All Services)

Start PostgreSQL, Odoo, and the Next.js portal together:

```bash
# From repository root
cp deployment/.env.example .env   # first time only
docker compose -f deployment/docker-compose.yml up -d
```

Check status:

```bash
docker compose ps
curl http://localhost:8069/api/health
curl http://localhost:3000/api/health
```

Stop everything:

```bash
./deployment/stop.sh
# or: docker compose down
```

### Portal via Docker only

```bash
./deployment/start-portal.sh docker
```

---

## Deploy Frontend to Vercel

```bash
cd student-portal
cp .env.example .env.local
npx vercel
```

### Vercel Environment Variables

| Variable | Example |
|----------|---------|
| `NEXT_PUBLIC_ODOO_URL` | `https://your-odoo.railway.app` |
| `NEXT_PUBLIC_ODOO_DB` | `student_admission` |

### Vercel Configuration (`student-portal/vercel.json`)

| Setting | Value |
|---------|-------|
| Framework | Next.js |
| Build Command | `npm run build` |
| Install Command | `npm install` |
| Output Directory | `.next` (auto for Next.js) |
| Root Directory | `student-portal` |

Production deploy:

```bash
cd student-portal
vercel --prod
```

---

## Deploy Odoo Backend

Odoo cannot run on Vercel. Use Docker on:

- **Railway** — deploy from `deployment/Dockerfile.odoo`
- **Render** — Docker web service + PostgreSQL
- **AWS EC2 / Azure VM** — `docker compose up -d` from repo root

Set environment variable on the Odoo host:

```
STUDENT_ADMISSION_CORS_ORIGINS=https://your-app.vercel.app,http://localhost:3000
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `docker: command not found` | Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) |
| Odoo health check timeout | Run `docker compose logs odoo` — first init takes several minutes |
| Port 8069 in use | Stop other Odoo instances or change port in `docker-compose.yml` |
| Port 3000 in use | `PORT=3001 npm run dev` or stop conflicting process |
| Portal cannot reach Odoo | Verify `NEXT_PUBLIC_ODOO_URL=http://localhost:8069` in `.env.local` |
| CORS errors in browser | Add your origin to `STUDENT_ADMISSION_CORS_ORIGINS` |
| Reset database | `docker compose down -v` then `./deployment/start.sh` |

---

## File Reference

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Root stack: postgres + odoo + portal |
| `deployment/start.sh` | Start backend (db + odoo) |
| `deployment/start-portal.sh` | Start portal (local npm or docker) |
| `deployment/stop.sh` | Stop all containers |
| `deployment/Dockerfile.odoo` | Odoo 17 image with module |
| `deployment/Dockerfile.portal` | Next.js production image |
| `deployment/entrypoint-odoo.sh` | DB creation + module install |
| `deployment/odoo.conf` | Odoo configuration |
| `deployment/.env.example` | Docker environment template |
| `student-portal/.env.example` | Portal environment template |
| `student-portal/vercel.json` | Vercel deployment config |
