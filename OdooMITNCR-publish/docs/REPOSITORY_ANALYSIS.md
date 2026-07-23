# Repository Analysis — OdooMITNCR

## Root cause of Vercel 404 NOT_FOUND

| Issue | Status | Fix |
|-------|--------|-----|
| **Repository was completely empty** | Fixed | Populated all 3 projects |
| No Next.js app at deploy root | Fixed | Root `vercel.json` + Root Directory docs |
| Legacy `builds` array pointing to wrong path | Fixed | Removed; uses `student-admission-portal-vercel` |
| `output: 'standalone'` breaking Vercel | N/A | Not present in portal config |

## Project identification

| Path | Role | Framework | Port |
|------|------|-----------|------|
| `student-admission-portal-vercel/` | **Frontend** | Next.js 14, React 18, Tailwind | 3000 |
| `student-admission-odoo-backend/` | **Odoo ERP** | Odoo 17, Python, PostgreSQL | 8069 |
| `server/` | **Banking REST API** | Express 5, Node.js, MongoDB | 5000 |

## Missing files (were missing — now created)

| File | Location | Purpose |
|------|----------|---------|
| `README.md` | Root | Monorepo overview |
| `vercel.json` | Root | Vercel monorepo build config |
| `package.json` | Root | Workspace scripts |
| `.gitignore` | Root | Ignore node_modules, .next, .env |
| `.env.example` | Root | Combined env reference |
| `docs/DEPLOYMENT.md` | docs/ | Railway, Render, VPS, Docker, Vercel |
| `docs/REPOSITORY_ANALYSIS.md` | docs/ | This file |
| `docs/FILE_TREE.txt` | docs/ | Complete file listing (171 files) |

## Broken files (fixed)

| File | Issue | Fix |
|------|-------|-----|
| `student-admission-portal-vercel/src/app/api/health/route.ts` | Always returned `status: ok` even when Odoo down | `healthy = odooStatus === 'ok'`, returns 503 when degraded |
| `student-admission-portal-vercel/next.config.js` | Invalid CORS combo (`*` + credentials); deprecated `images.domains` | Removed CORS headers; use `remotePatterns` |
| Root `vercel.json` (old monorepo) | Pointed to `student-portal/` (wrong path) | Points to `student-admission-portal-vercel/` |

## Build validation

| Check | Result |
|-------|--------|
| `npm ci` (portal) | Pass |
| `npm run build` (portal) | Pass — 12 routes compiled |
| `npm ci` (server) | Pass |
| `npm test` (server) | Pass — 18/18 tests |
| Broken imports | None found |
| Odoo `__manifest__.py` refs | All files present |

## Correct Vercel configuration

### Dashboard settings (recommended)

```
Root Directory:    student-admission-portal-vercel
Framework:         Next.js
Install Command:   npm install
Build Command:     npm run build
Output Directory:  .next
Node.js:           20.x
Region:            bom1 (Mumbai)
```

### Root vercel.json (fallback)

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "nextjs",
  "installCommand": "cd student-admission-portal-vercel && npm install",
  "buildCommand": "cd student-admission-portal-vercel && npm run build",
  "devCommand": "cd student-admission-portal-vercel && npm run dev",
  "outputDirectory": "student-admission-portal-vercel/.next",
  "regions": ["bom1"]
}
```

### Portal vercel.json

```json
{
  "framework": "nextjs",
  "regions": ["bom1"]
}
```

## Environment variables

### Frontend (Vercel)

```env
NEXT_PUBLIC_ODOO_URL=https://your-odoo-host.com
NEXT_PUBLIC_ODOO_DB=student_admission
```

### Odoo backend

```env
POSTGRES_USER=odoo
POSTGRES_PASSWORD=odoo
POSTGRES_DB=postgres
ODOO_DATABASE=student_admission
ODOO_DB_USER=odoo
STUDENT_ADMISSION_CORS_ORIGINS=https://your-app.vercel.app
```

### Banking API (server)

```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/ai-banking
JWT_SECRET=change-me
AI_SERVICE_URL=http://localhost:8000
BASE_URL=http://localhost:5000
```

## API connection map

```
Portal (browser) ──► Odoo /api/v1/*
  NEXT_PUBLIC_ODOO_URL + path

Portal /api/health ──► Odoo /api/health (server-side proxy)

Banking client ──► server /api/* (separate product, optional)
```

## Full file tree

See [FILE_TREE.txt](./FILE_TREE.txt) for all 171 files.

## Deployment commands

```bash
# Vercel (portal)
cd student-admission-portal-vercel && npm install && npm run build

# Odoo (Docker)
cd student-admission-odoo-backend && ./deployment/start.sh

# Banking API
cd server && npm install && npm start
```
