# Student Admission ERP — Run Scripts

One-click scripts to run the full stack locally.

## Prerequisites

| Tool | Linux/Mac | Windows |
|------|-----------|---------|
| Docker Desktop | Required for Odoo | Required for Odoo |
| Node.js 20+ | Required for portal | Required for portal |
| Git Bash (optional) | For `.sh` on Windows | Use `.bat` files |

Repo must contain:
- `student-admission-odoo-backend/`
- `student-admission-portal-vercel/`

---

## Quick start

### Linux / Mac / Git Bash

```bash
chmod +x scripts/student-admission/*.sh
./scripts/student-admission/setup.sh       # First time only
./scripts/student-admission/start-all.sh   # Odoo + Portal
```

### Windows (Command Prompt)

```cmd
scripts\student-admission\setup.bat
scripts\student-admission\start-all.bat
```

`start-all.bat` opens **two windows**: Odoo + Portal.

---

## Scripts reference

| Script | Purpose |
|--------|---------|
| `setup.sh` / `setup.bat` | Copy `.env` files, `npm install` |
| `start-odoo.sh` / `start-odoo.bat` | Start Odoo + PostgreSQL (Docker) |
| `start-portal.sh` / `start-portal.bat` | Start Next.js on port 3000 |
| `start-all.sh` / `start-all.bat` | Start everything |
| `stop-odoo.sh` / `stop-odoo.bat` | Stop Docker stack |
| `stop-all.sh` / `stop-all.bat` | Stop Odoo (+ close portal manually) |
| `verify.sh` / `verify.bat` | Health check both services |

---

## URLs after start

| Service | URL | Login |
|---------|-----|-------|
| Portal | http://localhost:3000 | rahul.sharma@example.com / demo123 |
| Odoo | http://localhost:8069 | admin / admin |
| Odoo API | http://localhost:8069/api/v1/courses | — |

---

## Manual two-terminal workflow

**Terminal 1 — Odoo:**
```bash
./scripts/student-admission/start-odoo.sh
```

**Terminal 2 — Portal:**
```bash
./scripts/student-admission/start-portal.sh
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Docker not found | Install Docker Desktop, restart PC |
| Port 8069 in use | `docker compose down` in odoo-backend folder |
| Port 3000 in use | Kill other Node process or change port in package.json |
| Odoo slow first run | Wait 3-5 minutes, check `docker compose logs odoo` |
| Portal can't reach Odoo | Ensure `.env.local` has `NEXT_PUBLIC_ODOO_URL=http://localhost:8069` |
