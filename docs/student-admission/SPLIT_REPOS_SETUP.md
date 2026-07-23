# Split Repos — Publish to GitHub & Vercel

The split directories are ready in this monorepo. Follow these steps to publish them as standalone repositories.

## Step 1: Create two empty GitHub repos

Create **empty** repositories (do not add README, .gitignore, or license):

| Repo | Create link |
|------|-------------|
| `student-admission-odoo-backend` | https://github.com/new?name=student-admission-odoo-backend&description=Odoo+17+Student+Admission+ERP+backend |
| `student-admission-portal-vercel` | https://github.com/new?name=student-admission-portal-vercel&description=Next.js+Student+Admission+portal+for+Vercel |

## Step 2: Push both repos

```bash
./scripts/push-split-repos.sh meenakshi25jan --push
```

Or manually:

```bash
cd student-admission-odoo-backend
git init -b main && git add . && git commit -m "Initial commit"
git remote add origin https://github.com/meenakshi25jan/student-admission-odoo-backend.git
git push -u origin main

cd ../student-admission-portal-vercel
git init -b main && git add . && git commit -m "Initial commit"
git remote add origin https://github.com/meenakshi25jan/student-admission-portal-vercel.git
git push -u origin main
```

## Step 3: Deploy portal on Vercel

1. Go to https://vercel.com/new
2. Import **`meenakshi25jan/student-admission-portal-vercel`** (NOT `ai-banking-platform`)
3. Framework: **Next.js** (auto-detected)
4. Root Directory: **`.`** (leave default — app is at repo root)
5. Region: **Mumbai (bom1)** (optional, already in `vercel.json`)

### Vercel environment variables

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_ODOO_URL` | Your Odoo backend URL (e.g. `https://odoo.example.com`) |
| `NEXT_PUBLIC_ODOO_DB` | `student_admission` |

## Step 4: Run Odoo backend

```bash
cd student-admission-odoo-backend
cp .env.example .env
./deployment/start.sh
```

Set on the Odoo host:

```
STUDENT_ADMISSION_CORS_ORIGINS=https://your-app.vercel.app
```

## Step 5: Verify

- Portal health: `https://your-app.vercel.app/api/health`
- Odoo health: `http://localhost:8069/api/health`
- Portal pages load without 404

## Optional: Clean up monorepo (after verifying split repos)

Remove duplicate paths from `ai-banking-platform`:

- `student_admission/`
- `student-portal/`
- `deployment/`
- `vercel.json` (root)
- `student-admission-odoo-backend/` and `student-admission-portal-vercel/` (copies)

Keep `docs/student-admission/SPLIT_ANALYSIS.md` as migration reference.
