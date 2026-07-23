# Student Admission ERP — Odoo 17 Backend

Odoo 17 backend for **Student Registration and Admission Management**.

This repository contains **only** the Odoo ERP backend — no frontend code.

## What's included

- `student_admission/` — Odoo 17 custom module
- `deployment/` — Docker, PostgreSQL, startup scripts
- `docs/` — API reference, deployment, testing guides
- `docker-compose.yml` — PostgreSQL + Odoo stack

## Quick start

```bash
cp .env.example .env
chmod +x deployment/start.sh
./deployment/start.sh
```

| Service | URL |
|---------|-----|
| Odoo | http://localhost:8069 |
| Health | http://localhost:8069/api/health |
| API | http://localhost:8069/api/v1/courses |
| PostgreSQL | localhost:5433 |

**Credentials:** `admin` / `admin`

## Connect the frontend

Deploy the companion portal repo: **student-admission-portal-vercel**

Set in Vercel:
```
NEXT_PUBLIC_ODOO_URL=https://your-odoo-host.com
NEXT_PUBLIC_ODOO_DB=student_admission
```

Set CORS on this backend:
```
STUDENT_ADMISSION_CORS_ORIGINS=https://your-portal.vercel.app
```

## Docker

```bash
docker compose up -d
docker compose logs -f odoo
```

## Module features

- Student registration & admission workflow
- Academic structure (campus, department, course, batch)
- Document verification & fee management
- REST API v1 with CORS
- Role-based security & reports

## Documentation

- [Running Guide](docs/RUNNING_GUIDE.md)
- [API Reference](docs/API.md)
- [Docker Deployment](docs/DOCKER_DEPLOYMENT.md)
- [Testing](docs/TESTING.md)

## License

LGPL-3
