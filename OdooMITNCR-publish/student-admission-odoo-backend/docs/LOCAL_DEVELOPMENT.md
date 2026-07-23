# Local Development Guide

## Prerequisites

- Python 3.10+, Node.js 18+, PostgreSQL 15+
- OR Docker & Docker Compose

## Option A: Docker (Recommended)

```bash
# 1. Start Odoo + PostgreSQL
chmod +x deployment/start.sh
./deployment/start.sh

# 2. Create database at http://localhost:8069
#    - Master password: admin
#    - Database name: student_admission
#    - Load demo data: Yes

# 3. Start Next.js portal
chmod +x deployment/start-portal.sh
./deployment/start-portal.sh
```

Portal: http://localhost:3000  
Odoo: http://localhost:8069

## Option B: Manual Setup

### Odoo Backend

```bash
# Clone Odoo 17, copy module
cp -r student_admission /path/to/odoo/addons/

# Configure odoo.conf addons_path
./odoo-bin -c odoo.conf -d student_admission -i student_admission --dev=all
```

### Next.js Portal

```bash
cd student-portal
cp .env.example .env.local
# Edit NEXT_PUBLIC_ODOO_URL and NEXT_PUBLIC_ODOO_DB
npm install
npm run dev
```

## Demo Users

| Role | Login | Password |
|------|-------|----------|
| Admin | admin | admin |
| Admission Officer | admission.officer@institute.edu | demo123 |
| Account Officer | accounts@institute.edu | demo123 |
| Student | rahul.sharma@example.com | demo123 |

## Environment Variables

### Portal (.env.local)
```
NEXT_PUBLIC_ODOO_URL=http://localhost:8069
NEXT_PUBLIC_ODOO_DB=student_admission
```

### Odoo (docker-compose)
```
STUDENT_ADMISSION_CORS_ORIGINS=http://localhost:3000,https://*.vercel.app
```
