# OdooMITNCR — Student Admission ERP Monorepo

MIT NCR Student Registration & Admission platform: **Next.js portal** (Vercel) + **Odoo 17 backend** (Docker) + **Express banking API** (optional).

## Repository structure

```
OdooMITNCR/
├── vercel.json                          # Vercel monorepo config (points to portal)
├── package.json                         # Root scripts (dev/build helpers)
├── .env.example                         # All env vars (all projects)
├── README.md
├── docs/
│   ├── DEPLOYMENT.md                    # Railway, Render, VPS, Docker, Vercel
│   └── REPOSITORY_ANALYSIS.md           # Full file inventory & fixes
│
├── student-admission-portal-vercel/       # FRONTEND — Next.js 14 (Vercel)
│   ├── package.json
│   ├── next.config.js
│   ├── vercel.json
│   ├── .env.example
│   └── src/app/                         # App Router pages
│
├── student-admission-odoo-backend/        # ODOO BACKEND — Odoo 17 + PostgreSQL
│   ├── docker-compose.yml
│   ├── deployment/                      # Dockerfile, odoo.conf, start.sh
│   ├── student_admission/               # Custom Odoo module
│   └── .env.example
│
└── server/                              # BANKING API — Express 5 + MongoDB
    ├── package.json
    ├── Dockerfile
    ├── .env.example
    └── src/server.js
```

## Project identification

| Folder | Type | Framework | Deploy target |
|--------|------|-----------|---------------|
| `student-admission-portal-vercel` | **Frontend** | Next.js 14, React 18, Tailwind | **Vercel** |
| `student-admission-odoo-backend` | **Odoo ERP** | Odoo 17, Python, PostgreSQL | Docker / Railway / VPS |
| `server` | **REST API** | Express 5, Node.js, MongoDB | Railway / Render / Docker |

## Quick start (local)

```bash
# 1. Odoo backend
cd student-admission-odoo-backend
cp .env.example .env
./deployment/start.sh          # http://localhost:8069

# 2. Next.js portal
cd ../student-admission-portal-vercel
cp .env.example .env.local
npm install && npm run dev     # http://localhost:3000

# 3. Banking API (optional)
cd ../server
cp .env.example .env
npm install && npm run dev     # http://localhost:5000
```

## Vercel deployment (fixes 404 NOT_FOUND)

**Root cause of 404:** Repository was empty OR Vercel deployed repo root without a Next.js app.

### Option A — Recommended (Vercel dashboard)

1. Import `meenakshi25jan/OdooMITNCR` in Vercel
2. Set **Root Directory** → `student-admission-portal-vercel`
3. Framework: **Next.js** (auto-detected)
4. Install: `npm install`
5. Build: `npm run build`
6. Output: `.next` (automatic)
7. Environment variables:
   - `NEXT_PUBLIC_ODOO_URL` = your Odoo HTTPS URL
   - `NEXT_PUBLIC_ODOO_DB` = `student_admission`

### Option B — Root vercel.json (no Root Directory change)

Root `vercel.json` is preconfigured with install/build commands pointing to the portal subdirectory.

## Environment variables

See `.env.example` and per-project `.env.example` files.

## Documentation

- [Full deployment guide](docs/DEPLOYMENT.md)
- [Repository analysis & fixes](docs/REPOSITORY_ANALYSIS.md)
- [Odoo API](student-admission-odoo-backend/docs/API.md)
- [Vercel portal guide](student-admission-portal-vercel/docs/VERCEL_DEPLOYMENT.md)
