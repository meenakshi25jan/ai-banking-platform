# Testing Guide — Student Admission ERP Platform

## 1. Odoo Unit Tests

```bash
./odoo-bin -c odoo.conf -d test_db \
  -i student_admission --test-enable --stop-after-init --log-level=test
```

### Test Coverage
- Registration sequence & workflow
- Full admission lifecycle (submit → verify → approve → pay → admit)
- Course seat availability
- Academic year validation

## 2. Portal Unit Tests

```bash
cd student-portal
npm install
npm test
```

## 3. Integration Testing (Manual)

### API Tests with curl

```bash
# Public: list courses
curl http://localhost:8069/api/v1/courses

# Public: create registration
curl -X POST http://localhost:8069/api/v1/registrations \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"t@example.com","mobile":"9000000001","date_of_birth":"2005-01-01","gender":"male","address":"Test","parent_name":"Parent","parent_mobile":"9000000002"}'

# Auth: login
curl -c cookies.txt -X POST http://localhost:8069/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin","password":"admin","db":"student_admission"}'

# Auth: dashboard
curl -b cookies.txt http://localhost:8069/api/v1/dashboard
```

### Portal E2E Checklist

| # | Test | Expected |
|---|------|----------|
| 1 | Home page loads | Hero, features visible |
| 2 | Courses page | Lists courses from API |
| 3 | Registration form | Returns registration number |
| 4 | Apply form | Creates admission application |
| 5 | Login | Redirects to dashboard |
| 6 | Dashboard | Shows KPI cards |
| 7 | Admission status | Shows workflow steps |
| 8 | Dark mode toggle | Theme switches |
| 9 | Mobile responsive | Layout adapts |

## 4. Security Testing

- [ ] Student portal user cannot see other students' records
- [ ] Account officer cannot modify course configuration
- [ ] Public API cannot access authenticated endpoints without session
- [ ] CORS blocks unauthorized origins

## 5. Deployment Verification

After deploying to Vercel + cloud Odoo:

```bash
# Frontend
curl -I https://your-app.vercel.app

# Backend
curl https://your-odoo.railway.app/api/v1/courses

# CORS
curl -H "Origin: https://your-app.vercel.app" \
  -X OPTIONS https://your-odoo.railway.app/api/v1/courses -v
```
