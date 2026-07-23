const ODOO_URL = process.env.NEXT_PUBLIC_ODOO_URL || 'http://localhost:8069';
const ODOO_DB = process.env.NEXT_PUBLIC_ODOO_DB || 'student_admission';

export interface ApiResponse<T> {
  status: string;
  data?: T;
  message?: string;
}

async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
): Promise<ApiResponse<T>> {
  const url = `${ODOO_URL}${path}`;
  const res = await fetch(url, {
    ...options,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  return res.json();
}

export const api = {
  login: (email: string, password: string) =>
    apiFetch<{ uid: number; name: string; email: string; session_id: string; registration_id: number | null }>(
      '/api/v1/auth/login',
      { method: 'POST', body: JSON.stringify({ email, password, db: ODOO_DB }) },
    ),

  me: () => apiFetch<{ uid: number; name: string; email: string; registration_id: number | null }>('/api/v1/auth/me'),

  logout: () => apiFetch('/api/v1/auth/logout', { method: 'POST' }),

  getCourses: () => apiFetch<Course[]>('/api/v1/courses'),

  getAcademicYears: () => apiFetch<AcademicYear[]>('/api/v1/academic-years'),

  createRegistration: (data: RegistrationPayload) =>
    apiFetch<{ id: number; registration_number: string; state: string }>(
      '/api/v1/registrations',
      { method: 'POST', body: JSON.stringify(data) },
    ),

  getRegistration: (id: number) => apiFetch<Registration>(`/api/v1/registrations/${id}`),

  getAdmissions: () => apiFetch<Admission[]>('/api/v1/admissions'),

  createAdmission: (data: AdmissionPayload) =>
    apiFetch<Admission>('/api/v1/admissions', { method: 'POST', body: JSON.stringify(data) }),

  getAdmission: (id: number) => apiFetch<AdmissionDetail>(`/api/v1/admissions/${id}`),

  getFees: (admissionId?: number) =>
    apiFetch<Fee[]>(`/api/v1/fees${admissionId ? `?admission_id=${admissionId}` : ''}`),

  getDashboard: () => apiFetch<DashboardData>('/api/v1/dashboard'),

  sendContact: (data: { name: string; email: string; message: string }) =>
    apiFetch('/api/v1/contact', { method: 'POST', body: JSON.stringify(data) }),
};

export interface Course {
  id: number;
  name: string;
  code: string;
  department: string;
  program: string;
  campus: string;
  duration_months: number;
  total_seats: number;
  available_seats: number;
  admission_fee: number;
  course_fee: number;
  eligibility_criteria: string;
}

export interface AcademicYear {
  id: number;
  name: string;
  code: string;
  current: boolean;
}

export interface RegistrationPayload {
  first_name: string;
  last_name: string;
  email: string;
  mobile: string;
  date_of_birth: string;
  gender: string;
  address: string;
  parent_name: string;
  parent_mobile: string;
  parent_email?: string;
  aadhaar_number?: string;
}

export interface Registration {
  id: number;
  registration_number: string;
  full_name: string;
  email: string;
  mobile: string;
  state: string;
}

export interface AdmissionPayload {
  registration_id: number;
  academic_year_id: number;
  course_id: number;
  merit_score?: number;
  auto_submit?: boolean;
}

export interface Admission {
  id: number;
  admission_number: string;
  student_name: string;
  state: string;
  course: string;
  department: string;
  total_fee: number;
  paid_fee: number;
  pending_fee: number;
}

export interface AdmissionDetail extends Admission {
  documents: { id: number; name: string; state: string; required: boolean }[];
  fees: { id: number; receipt_number: string; fee_type: string; amount: number; state: string }[];
}

export interface Fee {
  id: number;
  receipt_number: string;
  student_name: string;
  fee_type: string;
  amount: number;
  net_amount: number;
  state: string;
}

export interface DashboardData {
  total_students: number;
  total_applications: number;
  pending_admissions: number;
  approved_admissions: number;
  rejected_admissions: number;
  admitted_students: number;
  fee_collected: number;
  fee_pending: number;
  department_wise: { department: string; admissions: number }[];
  course_wise: { course: string; applications: number }[];
}
