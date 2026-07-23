# Docker Deployment Guide

## Quick Start

```bash
cd deployment
docker compose up -d --build
```

Services:
| Service | Port | Description |
|---------|------|-------------|
| odoo | 8069 | Odoo ERP backend |
| db | 5433 | PostgreSQL 15 |

## First-Time Setup

1. Open http://localhost:8069
2. Create database `student_admission` with demo data
3. Install **Student Admission ERP** module (auto-installed via compose command)

## Production Deployment

### docker-compose.prod.yml overrides

```yaml
services:
  odoo:
    environment:
      STUDENT_ADMISSION_CORS_ORIGINS: https://your-portal.vercel.app
    restart: always
  db:
    restart: always
```

### Persistent Volumes

Data is stored in Docker volumes:
- `odoo-db-data` — PostgreSQL data
- `odoo-web-data` — Odoo filestore

### Backup

```bash
docker compose exec db pg_dump -U odoo student_admission > backup.sql
```

### Restore

```bash
cat backup.sql | docker compose exec -T db psql -U odoo student_admission
```

## Cloud Deployment (AWS EC2)

```bash
# On Ubuntu 22.04
sudo apt update && sudo apt install -y docker.io docker-compose-plugin
git clone <your-repo> && cd <repo>/deployment
docker compose up -d --build
```

Open security group port 8069 (or use nginx reverse proxy with SSL).

## Nginx Reverse Proxy (SSL)

```nginx
server {
    listen 443 ssl;
    server_name erp.yourinstitute.edu;
    location / {
        proxy_pass http://127.0.0.1:8069;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
