'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { api, Course, AcademicYear } from '@/lib/api';
import { CheckCircle } from 'lucide-react';

export default function ApplyContent() {
  const params = useSearchParams();
  const [courses, setCourses] = useState<Course[]>([]);
  const [years, setYears] = useState<AcademicYear[]>([]);
  const [form, setForm] = useState({ registration_id: '', academic_year_id: '', course_id: params.get('course') || '', merit_score: '' });
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState<string | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    api.getCourses().then(r => r.data && setCourses(r.data));
    api.getAcademicYears().then(r => r.data && setYears(r.data));
  }, []);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true); setError('');
    const res = await api.createAdmission({
      registration_id: Number(form.registration_id),
      academic_year_id: Number(form.academic_year_id),
      course_id: Number(form.course_id),
      merit_score: form.merit_score ? Number(form.merit_score) : undefined,
      auto_submit: true,
    });
    if (res.status === 'success' && res.data) setDone(res.data.admission_number);
    else setError(res.message || 'Application failed');
    setLoading(false);
  };

  if (done) return (
    <div className="mx-auto max-w-lg px-4 py-20 text-center">
      <CheckCircle className="mx-auto text-green-500" size={64} />
      <h1 className="mt-6 text-3xl font-bold">Application Submitted!</h1>
      <p className="mt-3">Admission Number: <strong>{done}</strong></p>
    </div>
  );

  return (
    <div className="mx-auto max-w-xl px-4 py-16">
      <h1 className="text-4xl font-bold">Apply for Admission</h1>
      <p className="mt-3 text-gray-600">Enter your registration number and select a course.</p>
      {error && <p className="mt-4 rounded-lg bg-red-50 p-3 text-sm text-red-600">{error}</p>}
      <form onSubmit={submit} className="mt-8 space-y-4">
        <div><label className="label">Registration ID *</label>
          <input required className="input" placeholder="From registration confirmation" value={form.registration_id}
            onChange={e => setForm({...form, registration_id: e.target.value})} /></div>
        <div><label className="label">Academic Year *</label>
          <select required className="input" value={form.academic_year_id} onChange={e => setForm({...form, academic_year_id: e.target.value})}>
            <option value="">Select year</option>
            {years.map(y => <option key={y.id} value={y.id}>{y.name}</option>)}
          </select></div>
        <div><label className="label">Course *</label>
          <select required className="input" value={form.course_id} onChange={e => setForm({...form, course_id: e.target.value})}>
            <option value="">Select course</option>
            {courses.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select></div>
        <div><label className="label">Merit Score</label>
          <input type="number" className="input" value={form.merit_score} onChange={e => setForm({...form, merit_score: e.target.value})} /></div>
        <button type="submit" disabled={loading} className="btn-primary w-full">{loading ? 'Submitting...' : 'Submit Application'}</button>
      </form>
    </div>
  );
}
