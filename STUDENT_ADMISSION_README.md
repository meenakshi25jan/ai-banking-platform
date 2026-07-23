# Split Repository Notice

The Student Admission ERP has been split into two standalone repositories:

| Repository | Folder | Deploy to |
|------------|--------|-----------|
| **student-admission-odoo-backend** | `student-admission-odoo-backend/` | Docker / Railway / AWS |
| **student-admission-portal-vercel** | `student-admission-portal-vercel/` | Vercel |

See [docs/student-admission/SPLIT_ANALYSIS.md](docs/student-admission/SPLIT_ANALYSIS.md) for the full file mapping and GitHub push instructions.

**For Vercel:** Import `student-admission-portal-vercel` as a new project — do NOT deploy this monorepo.
