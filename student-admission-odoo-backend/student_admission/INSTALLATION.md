# Student Admission ERP — Installation & Module Guide

## Overview

**Module:** `student_admission`  
**Version:** 17.0.3.0.0  
**Odoo:** 17.x (compatible with 18 with minor manifest adjustments)  
**Database:** PostgreSQL  

Complete Student Registration and Admission Management for educational institutes.

---

## Installation

### Method 1 — Docker (recommended)

```bash
cd student-admission-odoo-backend   # or OdooMITNCR/student-admission-odoo-backend
cp .env.example .env
./deployment/start.sh
```

Open http://localhost:8069 → **Apps** → Update Apps List → search **Student Admission ERP** → **Install**.

### Method 2 — Existing Odoo server

```bash
# Copy module to addons path
cp -r student_admission /path/to/odoo/addons/

# Restart Odoo with addons path
./odoo-bin -c odoo.conf -d student_admission -i student_admission --without-demo=all
```

### Method 3 — With demo data

```bash
./odoo-bin -c odoo.conf -d student_admission -i student_admission --load-demo
```

---

## Post-installation setup

1. **Settings → Users** — Assign roles:
   - Admission Administrator
   - Admission Officer
   - Account Officer
   - Student (portal)

2. **Student Admission → Configuration → Academic Structure**
   - Create Campus → Department → Program → Course
   - Set academic year, batches, semesters

3. **Configuration → Document Checklist** — Verify default checklist items

4. **Settings → Technical → Email** — Configure outgoing mail server for notifications

---

## Module structure (file by file)

```
student_admission/
├── __init__.py                 # Loads models, controllers, wizards, reports
├── __manifest__.py             # Module metadata, dependencies, data files
├── INSTALLATION.md             # This guide
│
├── models/                     # ORM business logic
│   ├── student_registration.py    # Registration + documents + photo
│   ├── admission_application.py     # Admission workflow + fees trigger
│   ├── course.py                    # Courses, fees, seats, eligibility
│   ├── campus.py, department.py     # Academic hierarchy
│   ├── program.py, semester.py, batch.py
│   ├── academic_year.py
│   ├── document_verification.py     # Document checklist workflow
│   ├── fee_management.py            # Payments, receipts, reminders
│   ├── scholarship.py               # Scholarships and discounts
│   └── dashboard.py                 # KPI dashboard (transient)
│
├── security/
│   ├── security.xml            # 4 role groups + record rules
│   └── ir.model.access.csv     # CRUD permissions per model/role
│
├── views/                      # UI (form, tree, search, pivot, graph)
│   ├── menus.xml               # Main menu + Reports submenu (9 reports)
│   ├── student_registration_views.xml
│   ├── admission_application_views.xml
│   ├── document_verification_views.xml
│   ├── fee_views.xml, dashboard_views.xml
│   └── campus/department/program/course/... views
│
├── wizard/
│   ├── admission_reject_wizard.py   # Reject with reason + email
│   └── document_reject_wizard.py    # Reject document with remarks
│
├── report/
│   ├── admission_reports.xml   # PDF report actions
│   ├── report_templates.xml    # QWeb PDF templates
│   └── admission_report.py     # Report helpers
│
├── data/
│   ├── sequence_data.xml       # REG/, ADM/, RCPT/ sequences
│   ├── document_checklist_data.xml
│   ├── mail_template_data.xml  # 7 email templates
│   └── cron_data.xml           # Daily fee due reminder
│
├── controllers/
│   ├── api_v1.py               # REST API /api/v1/*
│   ├── cors.py                 # CORS for Next.js portal
│   └── main.py                 # Health check /api/health
│
├── demo/
│   ├── demo_data.xml           # Sample campus, courses, year
│   └── demo_users.xml          # Demo users (password: demo123)
│
└── tests/
    ├── test_student_admission.py
    └── test_api_integration.py
```

---

## Features mapped to requirements

| # | Requirement | Implementation |
|---|-------------|----------------|
| 1 | Student Registration | `student.registration` — all fields, photo, documents, sequence on confirm |
| 2 | Admission Management | `student.admission.application` — 7-state workflow |
| 3 | Course Management | `student.course` — fees, duration, seats, min merit score |
| 4 | Academic Structure | Campus → Dept → Program → Course → Semester → Batch |
| 5 | Document Verification | Checklist + approve/reject wizards |
| 6 | Fee Management | `student.fee.payment` — receipts, PDF, cron reminders |
| 7 | User Roles | Admin, Officer, Account Officer, Student (portal) |
| 8 | Dashboard | `student.admission.dashboard` — KPIs + drill-down |
| 9 | Reports | 9 report menus (PDF + pivot/list) |
| 10 | Notifications | 7 email templates + daily fee cron |

---

## Admission workflow

```
Draft → Submitted → Under Review → Verified → Approved → Admitted
                              ↘ Rejected
```

| State | Action button | Email sent |
|-------|---------------|------------|
| Draft | Submit | — |
| Submitted | Under Review | Application Submitted |
| Under Review | Verify / Approve | — |
| Verified | Approve | — |
| Approved | Admit (after fees paid) | Admission Approval |
| Admitted | — | Admission Complete |
| Any (before approved) | Reject | Rejection |

---

## Demo credentials

| Login | Password | Role |
|-------|----------|------|
| admin | admin | Administrator |
| admission.officer@institute.edu | demo123 | Admission Officer |
| accounts@institute.edu | demo123 | Account Officer |
| rahul.sharma@example.com | demo123 | Student |

---

## REST API (optional)

Base URL: `http://localhost:8069/api/v1`

| Endpoint | Method | Auth |
|----------|--------|------|
| `/api/health` | GET | No |
| `/api/v1/auth/login` | POST | No |
| `/api/v1/courses` | GET | No |
| `/api/v1/registrations` | POST | No |
| `/api/v1/admissions` | GET/POST | User |
| `/api/v1/fees` | GET | User |
| `/api/v1/dashboard` | GET | User |

See `docs/API.md` for full API documentation.

---

## Running tests

```bash
# Inside Odoo container
odoo -d student_admission --test-enable -i student_admission --stop-after-init
```

---

## SMS notifications (optional)

Email notifications are built-in. For SMS, install Odoo **SMS** module (Enterprise) or integrate a third-party SMS gateway via a custom controller.

---

## Upgrade

```bash
./odoo-bin -c odoo.conf -d student_admission -u student_admission
```

---

## Support

- API docs: `docs/API.md`
- Docker: `docs/DOCKER_DEPLOYMENT.md`
- Vercel portal: see `student-admission-portal-vercel` in monorepo
