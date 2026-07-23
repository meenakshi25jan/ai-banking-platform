# Student Admission ERP

Production-ready Odoo 17 module for **Student Registration and Admission Management**.

## Features

- Student registration with auto-generated registration numbers
- Admission workflow: Draft → Submitted → Under Review → Approved → Rejected → Admitted
- Academic structure: Campus, Department, Program, Course, Semester, Batch, Academic Year
- Document verification checklist and approval workflow
- Fee management with receipts and pending fee tracking
- Role-based security (Administrator, Admission Officer, Account Officer, Student)
- Admission dashboard with KPIs
- PDF reports and analytics (graph/pivot views)
- Email notifications (registration, approval, rejection, fee reminders)
- REST API endpoints for integrations

## Requirements

- Odoo 17.0 (compatible with 18.0 with minor view adjustments)
- PostgreSQL
- Python 3.10+

## Installation

### 1. Copy the module

Copy the `student_admission` folder into your Odoo addons path:

```bash
cp -r student_admission /path/to/odoo/addons/
```

### 2. Update Odoo configuration

Add the addons path to `odoo.conf` if not already present:

```ini
[options]
addons_path = /path/to/odoo/addons,/path/to/custom/addons
```

### 3. Restart Odoo and update apps list

```bash
./odoo-bin -c odoo.conf -u base --stop-after-init
./odoo-bin -c odoo.conf
```

In the Odoo UI: **Apps → Update Apps List → Search "Student Admission ERP" → Install**

### 4. Load demo data (optional)

Enable demo data during database creation, or reinstall the module with demo data enabled.

### 5. Assign user roles

Go to **Settings → Users** and assign one of:

| Group | Permissions |
|-------|-------------|
| Admission Administrator | Full access |
| Admission Officer | Registrations, admissions, document verification |
| Account Officer | Fee collection and payments |
| Student | Portal access to own records |

## Module Structure

```
student_admission/
├── __init__.py
├── __manifest__.py
├── models/              # ORM business logic
├── security/            # Groups, access rights, record rules
├── views/               # Form, tree, search, dashboard views
├── wizard/              # Rejection wizards
├── report/              # QWeb PDF reports
├── data/                # Sequences, mail templates, cron jobs
├── controllers/         # REST API
├── demo/                # Sample data
├── tests/               # Unit tests
└── static/description/  # Module icon
```

## Workflow

### Student Registration

1. Create a registration record with personal and parent details
2. Upload photograph and supporting documents
3. Click **Confirm Registration** → registration number is generated and confirmation email is sent

### Admission Application

1. From a registered student, create an admission application
2. Select academic year, course, department (auto-filled)
3. Submit application → document checklist is auto-created
4. Upload and verify documents
5. Approve application → fee lines are created
6. Register fee payments
7. Admit student when all fees are paid

## REST API (Optional)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/student/admissions` | GET | List all admissions |
| `/api/student/admissions/<id>` | GET | Get admission details |
| `/api/student/registrations` | POST (JSON) | Create registration |

Authentication: Odoo user session (auth='user').

## Running Tests

```bash
./odoo-bin -c odoo.conf -d test_db -i student_admission --test-enable --stop-after-init
```

## Reports

- Student Registration Report (PDF)
- Admission Summary Report (PDF)
- Fee Collection Report (PDF)
- Department-wise / Course-wise analytics via pivot and graph views
- Pending verification and pending fee list views

## Notifications

| Event | Email Template |
|-------|----------------|
| Registration confirmed | Registration Confirmation |
| Admission approved | Admission Approval |
| Admission rejected | Admission Rejection |
| Fee due (cron daily) | Fee Due Reminder |

## License

LGPL-3
