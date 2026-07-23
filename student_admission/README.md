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

## How to Test

### Prerequisites

1. Install the module on a test database (with demo data enabled for quicker setup).
2. Create or use test users for each role:
   - **Admission Administrator** (full access)
   - **Admission Officer** (registrations & verification)
   - **Account Officer** (fees only)
   - **Student** (portal user)
3. Configure an **Outgoing Mail Server** under Settings if you want to verify email notifications.

---

### 1. Automated Unit Tests

Run all module tests on a fresh database:

```bash
./odoo-bin -c odoo.conf -d student_admission_test \
  -i student_admission \
  --test-enable \
  --stop-after-init \
  --log-level=test
```

Run only this module's tests (after the module is installed):

```bash
./odoo-bin -c odoo.conf -d student_admission_test \
  --test-enable \
  --stop-after-init \
  -u student_admission \
  --log-level=test
```

**What is covered by unit tests** (`tests/test_student_admission.py`):

| Test Class | Validates |
|------------|-----------|
| `TestStudentRegistration` | Sequence generation, registration workflow, full name compute |
| `TestAdmissionApplication` | Full admission flow: submit → verify docs → approve → pay fees → admit |
| `TestCourseManagement` | Available seats calculation, academic year date validation |

**Expected result:** All tests pass with no errors in the log. Look for lines like:

```
odoo.tests.common: Starting TestStudentRegistration.test_registration_workflow ...
```

---

### 2. Manual UI Testing (End-to-End)

Use demo data or create records manually. Follow this checklist:

#### A. Academic Setup

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Go to **Student Admission → Configuration → Campuses** | Campus list opens |
| 2 | Create campus, department, program, course | Records save with unique codes |
| 3 | Create academic year and mark as **Current** | Only one year can be current |
| 4 | Create a batch linked to course + academic year | Batch appears in admission form |

#### B. Student Registration

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Go to **Operations → Student Registrations → Create** | New draft registration |
| 2 | Fill personal info, parent details, upload photo | Form saves |
| 3 | Add supporting documents in the Documents tab | Documents attach |
| 4 | Click **Confirm Registration** | State → Registered, number like `REG/2026/00001` |
| 5 | Check student email (if mail server configured) | Registration confirmation email received |

#### C. Admission Application

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | From registration, click **Create Admission** | Admission form opens pre-filled |
| 2 | Select academic year and course, save | Document checklist auto-created |
| 3 | Click **Submit** | State → Submitted |
| 4 | Click **Under Review** | State → Under Review |
| 5 | Upload docs on each verification line, click **Submit** then **Approve** | All required docs → Approved |
| 6 | Click **Approve** | State → Approved, fee lines created |
| 7 | Go to Fee Payments tab, **Register Payment** for each fee | Fees → Paid |
| 8 | Click **Admit Student** | State → Admitted |

#### D. Rejection Flow

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Create a new submitted application | State = Submitted |
| 2 | Click **Reject**, enter reason | State → Rejected, rejection email sent |
| 3 | Reject a document via **Reject** wizard | Document state → Rejected with remarks |

#### E. Dashboard & Reports

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open **Student Admission → Dashboard** | KPIs show correct counts |
| 2 | Click stat buttons (Pending, Approved, etc.) | Filtered list views open |
| 3 | Open **Reports → Admission Summary Report** | Pivot/graph views load |
| 4 | Print PDF from a registration or admission form | PDF generates correctly |

---

### 3. Security & Role Testing

Log in as each test user and verify access:

| Role | Should Access | Should NOT Access |
|------|---------------|-------------------|
| Admission Officer | Registrations, admissions, document verification | Fee payment registration (write) |
| Account Officer | Fee payments, pending fees, dashboard | Course/campus configuration |
| Student (portal) | Own registration, own applications, upload docs | Other students' records |
| Administrator | Everything | — |

**Portal student test:**

1. Create a portal user and link to a registration (`user_id` field).
2. Assign the **Student** security group.
3. Log in at `/my` and confirm the student sees only their own records.

---

### 4. REST API Testing

Log in to Odoo in a browser first to obtain a session, then use the session cookie in API calls.

**List admissions:**

```bash
curl -b cookies.txt -c cookies.txt \
  "http://localhost:8069/api/student/admissions"
```

**Get admission detail:**

```bash
curl -b cookies.txt \
  "http://localhost:8069/api/student/admissions/1"
```

**Create registration (JSON-RPC style):**

```bash
curl -b cookies.txt -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "first_name": "Test",
      "last_name": "User",
      "email": "testuser@example.com",
      "mobile": "9000000099",
      "date_of_birth": "2005-06-15",
      "gender": "male",
      "address": "123 Test Street",
      "parent_name": "Parent User",
      "parent_mobile": "9000000088"
    },
    "id": 1
  }' \
  "http://localhost:8069/api/student/registrations"
```

**Expected result:** JSON response with `"status": "success"` and a generated registration number.

---

### 5. Email Notification Testing

| Trigger | How to Test | Expected Email |
|---------|-------------|----------------|
| Registration confirmed | Confirm a draft registration | Registration Confirmation |
| Admission approved | Approve a fully verified application | Admission Approval |
| Admission rejected | Reject via wizard with reason | Admission Rejection |
| Fee due reminder | Set fee `due_date` within 7 days, run cron manually | Fee Due Reminder |

**Run fee reminder cron manually** (Developer Mode → Settings → Technical → Scheduled Actions → *Student Admission: Fee Due Reminder* → Run Manually).

Or from Odoo shell:

```python
env['student.fee.payment']._cron_send_fee_due_reminders()
```

---

### 6. Demo Data Verification

If installed with demo data, confirm these records exist:

- **Campus:** Main Campus (`CAMP-MAIN`)
- **Courses:** BCA-101, MBA-101
- **Registration:** Rahul Sharma (registered)
- **Admission:** Submitted application for BCA

Navigate to **Student Admission** menu and verify counts on the dashboard match the demo records.

---

### 7. Common Issues & Troubleshooting

| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| Cannot approve admission | Required documents not approved | Approve all required verification lines first |
| Cannot admit student | Pending fees remain | Register payment for all fee lines |
| No seats available | Course capacity reached | Increase `total_seats` on the course |
| Emails not sent | Mail server not configured | Set up outgoing mail in Settings |
| Portal user sees nothing | `user_id` not set on registration | Link portal user to registration record |
| Aadhaar duplicate error | Unique constraint | Use a unique Aadhaar/identity number per student |

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
