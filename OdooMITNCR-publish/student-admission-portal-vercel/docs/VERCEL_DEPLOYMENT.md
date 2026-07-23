# Vercel Deployment — Student Admission Portal

This repository is **Vercel-ready**. No Odoo files, no monorepo configuration needed.

## Deploy

### Option A — Vercel Dashboard (recommended)

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import **student-admission-portal-vercel** repository
3. Framework: **Next.js** (auto-detected)
4. Root Directory: **/** (leave default)
5. Add environment variables (see below)
6. Deploy

### Option B — CLI

```bash
cp .env.example .env.local
chmod +x deploy-vercel.sh
./deploy-vercel.sh
```

## Environment variables

| Variable | Example |
|----------|---------|
| `NEXT_PUBLIC_ODOO_URL` | `https://your-odoo.railway.app` |
| `NEXT_PUBLIC_ODOO_DB` | `student_admission` |

Redeploy after changing env vars.

## Verify

```bash
curl https://YOUR-APP.vercel.app/api/health
curl -I https://YOUR-APP.vercel.app/
```

## Backend CORS

On your Odoo backend (`student-admission-odoo-backend`), set:

```
STUDENT_ADMISSION_CORS_ORIGINS=https://YOUR-APP.vercel.app
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| 404 NOT_FOUND | You deployed the wrong repo — use this repo only |
| API errors | Check `NEXT_PUBLIC_ODOO_URL` points to live Odoo |
| CORS errors | Add Vercel URL to backend `STUDENT_ADMISSION_CORS_ORIGINS` |
