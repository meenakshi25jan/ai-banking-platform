# Vercel Deployment Guide

## 1. Deploy Frontend to Vercel

```bash
cd student-portal
npx vercel
```

Or connect your GitHub repo in the [Vercel Dashboard](https://vercel.com):
- **Root Directory:** `student-portal`
- **Framework:** Next.js
- **Build Command:** `npm run build`
- **Output Directory:** `.next`

## 2. Environment Variables (Vercel Dashboard)

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_ODOO_URL` | `https://your-odoo-backend.railway.app` |
| `NEXT_PUBLIC_ODOO_DB` | `student_admission` |

## 3. Deploy Odoo Backend

Odoo cannot run on Vercel (needs persistent process + PostgreSQL). Deploy to:

| Platform | Notes |
|----------|-------|
| **Railway** | Use `deployment/docker-compose.yml`, expose port 8069 |
| **Render** | Docker web service + PostgreSQL add-on |
| **AWS EC2** | `docker compose up` on t3.medium+ |
| **Azure** | Container Instances + Azure Database for PostgreSQL |

### Railway Quick Start

1. Create new project → Deploy from GitHub
2. Add PostgreSQL service
3. Add web service with `deployment/Dockerfile.odoo`
4. Set env: `HOST`, `USER`, `PASSWORD` from PostgreSQL
5. Set `STUDENT_ADMISSION_CORS_ORIGINS=https://your-app.vercel.app`

## 4. Connect Frontend to Backend

1. Deploy Odoo and note the public URL
2. Set `NEXT_PUBLIC_ODOO_URL` in Vercel
3. Redeploy Vercel frontend
4. In Odoo, ensure CORS allows your Vercel domain

## 5. Verify Deployment

```bash
# Test Odoo API
curl https://your-odoo.railway.app/api/v1/courses

# Test portal
open https://your-app.vercel.app/courses
```

Checklist:
- [ ] Courses page loads data from Odoo
- [ ] Registration form submits successfully
- [ ] Login works with demo student credentials
- [ ] Dashboard shows KPI data

## 6. Custom Domain

In Vercel: Settings → Domains → Add your domain.

Update Odoo CORS:
```
STUDENT_ADMISSION_CORS_ORIGINS=https://admissions.yourinstitute.edu
```
