# Student Admission ERP — API Documentation

Base URL: `{ODOO_URL}/api/v1`

All responses follow: `{ "status": "success"|"error", "data": ..., "message": "..." }`

CORS is enabled for `localhost:3000` and `*.vercel.app`.

---

## Authentication

### POST `/api/v1/auth/login`
```json
{ "email": "student@example.com", "password": "secret", "db": "student_admission" }
```
**Response:** `{ uid, name, email, session_id, registration_id }`

### GET `/api/v1/auth/me` (auth required)
Returns current user profile.

### POST `/api/v1/auth/logout` (auth required)

---

## Public Endpoints

### GET `/api/v1/courses`
List all active courses with fees and seat availability.

### GET `/api/v1/academic-years`
List active academic years.

### POST `/api/v1/registrations`
Create student registration (public).
```json
{
  "first_name": "Rahul", "last_name": "Sharma",
  "email": "rahul@example.com", "mobile": "9876543210",
  "date_of_birth": "2005-03-15", "gender": "male",
  "address": "Pune", "parent_name": "Anil Sharma",
  "parent_mobile": "9876543211"
}
```

### POST `/api/v1/contact`
Submit contact form.

---

## Authenticated Endpoints

### GET `/api/v1/registrations/:id`
Get registration details.

### GET/POST `/api/v1/admissions`
List or create admission applications.

### GET `/api/v1/admissions/:id`
Get admission with documents and fees.

### GET `/api/v1/fees?admission_id=1`
List fee payments.

### GET `/api/v1/dashboard`
Admin KPIs: students, applications, fees, department/course stats.

---

## Legacy Endpoints (v0)

| Endpoint | Method |
|----------|--------|
| `/api/student/admissions` | GET |
| `/api/student/admissions/:id` | GET |
| `/api/student/registrations` | POST (JSON-RPC) |
