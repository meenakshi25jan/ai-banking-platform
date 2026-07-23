# Deployment Guide — OdooMITNCR

## 1. Frontend — Vercel (student-admission-portal-vercel)

### Vercel project settings

| Setting | Value |
|---------|-------|
| **Root Directory** | `student-admission-portal-vercel` |
| **Framework** | Next.js |
| **Install Command** | `npm install` |
| **Build Command** | `npm run build` |
| **Output Directory** | `.next` (default, auto) |
| **Node.js Version** | 20.x |

### Environment variables (Vercel dashboard)

| Variable | Example | Required |
|----------|---------|----------|
| `NEXT_PUBLIC_ODOO_URL` | `https://odoo.yourdomain.com` | Yes |
| `NEXT_PUBLIC_ODOO_DB` | `student_admission` | Yes |

### vercel.json (in portal folder)

```json
{
  "framework": "nextjs",
  "regions": ["bom1"]
}
```

### Deploy commands

```bash
cd student-admission-portal-vercel
npm install
npm run build
npx vercel --prod
```

---

## 2. Odoo Backend — Docker (student-admission-odoo-backend)

### Local / VPS

```bash
cd student-admission-odoo-backend
cp .env.example .env
./deployment/start.sh
```

| Service | URL |
|---------|-----|
| Odoo | http://localhost:8069 |
| Health | http://localhost:8069/api/health |
| API | http://localhost:8069/api/v1/* |
| PostgreSQL | localhost:5433 |

### Environment variables

```env
POSTGRES_USER=odoo
POSTGRES_PASSWORD=odoo
POSTGRES_DB=postgres
ODOO_DATABASE=student_admission
ODOO_DB_USER=odoo
STUDENT_ADMISSION_CORS_ORIGINS=https://your-app.vercel.app
```

---

## 3. Odoo Backend — Railway

1. Create new project → **Deploy from GitHub** → `OdooMITNCR`
2. Set **Root Directory** → `student-admission-odoo-backend`
3. Add **PostgreSQL** plugin
4. Set environment variables from `.env.example`
5. Use Dockerfile: `deployment/Dockerfile`
6. Expose port **8069**
7. Set `STUDENT_ADMISSION_CORS_ORIGINS` to your Vercel URL

### railway.toml (optional)

```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "deployment/Dockerfile"

[deploy]
startCommand = "/entrypoint-custom.sh odoo"
healthcheckPath = "/api/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
```

---

## 4. Odoo Backend — Render

1. New **Web Service** → connect `OdooMITNCR`
2. Root Directory: `student-admission-odoo-backend`
3. Environment: **Docker**
4. Dockerfile path: `deployment/Dockerfile`
5. Add **PostgreSQL** database
6. Set env vars; map `DATABASE_URL` to Odoo DB settings in entrypoint

---

## 5. Odoo Backend — VPS (Ubuntu)

```bash
# On VPS
git clone https://github.com/meenakshi25jan/OdooMITNCR.git
cd OdooMITNCR/student-admission-odoo-backend
cp .env.example .env
# Edit .env with production passwords and CORS origins

# Install Docker
curl -fsSL https://get.docker.com | sh
docker compose up -d --build

# Nginx reverse proxy (HTTPS)
sudo apt install nginx certbot python3-certbot-nginx
# Point odoo.yourdomain.com → localhost:8069
```

---

## 6. Banking API — server (Express)

### Docker

```bash
cd server
cp .env.example .env
docker build -t odoomitncr-server .
docker run -p 5000:5000 --env-file .env odoomitncr-server
```

### Railway / Render

| Setting | Value |
|---------|-------|
| Root Directory | `server` |
| Build | `npm ci --omit=dev` |
| Start | `node src/server.js` |
| Port | `5000` |

### Required env vars

```env
PORT=5000
MONGODB_URI=mongodb+srv://...
JWT_SECRET=your-secret
AI_SERVICE_URL=https://your-ai-service
```

---

## 7. End-to-end production wiring

```
[Vercel Portal]                    [Odoo Host]
NEXT_PUBLIC_ODOO_URL ──────────────► https://odoo.example.com
NEXT_PUBLIC_ODOO_DB  ──────────────► student_admission

[Odoo Host]
STUDENT_ADMISSION_CORS_ORIGINS ────► https://your-app.vercel.app
```

## 8. Validation checklist

- [ ] `cd student-admission-portal-vercel && npm install && npm run build`
- [ ] `cd server && npm install && npm test`
- [ ] `cd student-admission-odoo-backend && docker compose up -d`
- [ ] `curl http://localhost:8069/api/health`
- [ ] `curl http://localhost:3000/api/health`
- [ ] Vercel deploy succeeds with Root Directory = `student-admission-portal-vercel`
- [ ] Portal loads without 404 NOT_FOUND
