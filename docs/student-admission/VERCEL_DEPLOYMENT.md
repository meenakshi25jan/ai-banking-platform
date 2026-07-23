# Vercel Deployment Guide

## Fix: 404 NOT_FOUND on Vercel

This error means Vercel deployed the **wrong directory** or used **standalone output** (now fixed).

### Required fix (choose one)

**Option A — Set Root Directory (recommended for Git deploys)**

1. Open [Vercel Dashboard](https://vercel.com) → your project
2. **Settings → General → Root Directory**
3. Set to: `student-portal`
4. Click **Save**
5. **Deployments → Redeploy** (without cache)

**Option B — Deploy from portal folder (CLI)**

```bash
cd student-portal
chmod +x deploy-vercel.sh
./deploy-vercel.sh
```

**Option C — Deploy from repo root (uses root vercel.json)**

```bash
vercel --prod
```

Root `vercel.json` uses `@vercel/next` builder pointed at `student-portal/`.

---

## 1. Deploy Frontend to Vercel

```bash
cd student-portal
npx vercel --prod
```

Or connect GitHub repo with:
- **Root Directory:** `student-portal` ← **CRITICAL**
- **Framework:** Next.js (auto-detected)
- **Build Command:** `npm run build` (default)
- **Output Directory:** leave empty (auto)

> Do **NOT** set Output Directory manually — Vercel handles `.next` automatically.

## 2. Environment Variables (Vercel Dashboard)

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_ODOO_URL` | `https://your-odoo-backend.railway.app` |
| `NEXT_PUBLIC_ODOO_DB` | `student_admission` |

## 3. Verify Deployment

After redeploy, these must work:

```bash
curl https://your-app.vercel.app/api/health
# Expected: {"status":"ok","service":"student-admission-portal",...}

curl -I https://your-app.vercel.app/
# Expected: HTTP/2 200
```

Checklist:
- [ ] Home page loads (not 404)
- [ ] `/api/health` returns JSON
- [ ] `/courses` page loads
- [ ] `NEXT_PUBLIC_ODOO_URL` points to live Odoo backend

## 4. Deploy Odoo Backend

Odoo cannot run on Vercel. Deploy to Railway, Render, or AWS using `deployment/Dockerfile.odoo`.

Set on Odoo host:
```
STUDENT_ADMISSION_CORS_ORIGINS=https://your-app.vercel.app
```

## 5. Connect Frontend to Backend

1. Deploy Odoo and note the public URL
2. Set `NEXT_PUBLIC_ODOO_URL` in Vercel → Environment Variables
3. **Redeploy** the Vercel project (env vars require redeploy)
4. Confirm CORS on Odoo allows your Vercel domain

## 6. Custom Domain

Vercel → Settings → Domains → Add domain.

Update Odoo CORS:
```
STUDENT_ADMISSION_CORS_ORIGINS=https://admissions.yourinstitute.edu
```
