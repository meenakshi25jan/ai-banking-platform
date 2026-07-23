# Student Admission Portal — Next.js Frontend

Modern web portal for **Student Registration and Admission**. Deployable on **Vercel** with zero Odoo backend files.

## What's included

- Next.js 14 App Router + Tailwind CSS
- Student registration, admission, dashboard pages
- Dark/light mode, responsive design
- Odoo REST API client (`src/lib/api.ts`)

## Quick start (local)

```bash
cp .env.example .env.local
npm install
npm run dev
```

Open http://localhost:3000

> Requires the [Odoo backend](https://github.com/YOUR_ORG/student-admission-odoo-backend) running on port 8069.

## Deploy to Vercel

### 1. Import this repository in Vercel

- **Framework:** Next.js (auto-detected)
- **Root Directory:** `/` (repository root)
- **Build Command:** `npm run build`
- No custom output directory needed

### 2. Set environment variables

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_ODOO_URL` | Your Odoo backend URL |
| `NEXT_PUBLIC_ODOO_DB` | `student_admission` |

### 3. Deploy

```bash
chmod +x deploy-vercel.sh
./deploy-vercel.sh
```

Or push to `main` — Vercel auto-deploys.

## Pages

| Route | Description |
|-------|-------------|
| `/` | Home |
| `/courses` | Course listing (from Odoo API) |
| `/register` | Student registration |
| `/apply` | Admission application |
| `/login` | Student login |
| `/dashboard` | Student dashboard |
| `/admission-status` | Application tracker |
| `/api/health` | Health check |

## Backend connection

This portal connects to the Odoo backend via:

```
NEXT_PUBLIC_ODOO_URL/api/v1/*
```

Ensure CORS is configured on the backend:
```
STUDENT_ADMISSION_CORS_ORIGINS=https://your-app.vercel.app
```

## Documentation

- [Vercel Deployment Guide](docs/VERCEL_DEPLOYMENT.md)

## License

MIT
