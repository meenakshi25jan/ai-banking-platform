'use client';

import { useState } from 'react';
import { api } from '@/lib/api';
import { CheckCircle } from 'lucide-react';
import Link from 'next/link';

export default function RegisterPage() {
  const [form, setForm] = useState({
    first_name: '', last_name: '', email: '', mobile: '',
    date_of_birth: '', gender: 'male', address: '',
    parent_name: '', parent_mobile: '', parent_email: '', aadhaar_number: '',
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ number: string } | null>(null);
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    const res = await api.createRegistration(form);
    if (res.status === 'success' && res.data) {
      setResult({ number: res.data.registration_number });
    } else {
      setError(res.message || 'Registration failed');
    }
    setLoading(false);
  };

  if (result) {
    return (
      <div className="mx-auto max-w-lg px-4 py-20 text-center">
        <CheckCircle className="mx-auto text-green-500" size={64} />
        <h1 className="mt-6 text-3xl font-bold">Registration Successful!</h1>
        <p className="mt-3 text-gray-600 dark:text-gray-400">
          Your registration number is <strong className="text-brand-600">{result.number}</strong>
        </p>
        <Link href="/apply" className="btn-primary mt-8 inline-flex">Apply for Admission</Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-2xl px-4 py-16 sm:px-6 lg:px-8">
      <h1 className="text-4xl font-bold">Student Registration</h1>
      <p className="mt-3 text-gray-600 dark:text-gray-400">Fill in your details to create a student profile.</p>
      {error && <p className="mt-4 rounded-lg bg-red-50 p-3 text-sm text-red-600">{error}</p>}
      <form onSubmit={handleSubmit} className="mt-8 space-y-6">
        <div className="grid gap-4 sm:grid-cols-2">
          <div><label className="label">First Name *</label><input name="first_name" required className="input" value={form.first_name} onChange={handleChange} /></div>
          <div><label className="label">Last Name *</label><input name="last_name" required className="input" value={form.last_name} onChange={handleChange} /></div>
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          <div><label className="label">Email *</label><input name="email" type="email" required className="input" value={form.email} onChange={handleChange} /></div>
          <div><label className="label">Mobile *</label><input name="mobile" required className="input" value={form.mobile} onChange={handleChange} /></div>
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          <div><label className="label">Date of Birth *</label><input name="date_of_birth" type="date" required className="input" value={form.date_of_birth} onChange={handleChange} /></div>
          <div><label className="label">Gender *</label>
            <select name="gender" className="input" value={form.gender} onChange={handleChange}>
              <option value="male">Male</option><option value="female">Female</option><option value="other">Other</option>
            </select>
          </div>
        </div>
        <div><label className="label">Address *</label><textarea name="address" required className="input" rows={3} value={form.address} onChange={handleChange} /></div>
        <div><label className="label">Aadhaar / Identity Number</label><input name="aadhaar_number" className="input" value={form.aadhaar_number} onChange={handleChange} /></div>
        <h2 className="text-lg font-semibold">Parent / Guardian</h2>
        <div className="grid gap-4 sm:grid-cols-2">
          <div><label className="label">Name *</label><input name="parent_name" required className="input" value={form.parent_name} onChange={handleChange} /></div>
          <div><label className="label">Mobile *</label><input name="parent_mobile" required className="input" value={form.parent_mobile} onChange={handleChange} /></div>
        </div>
        <div><label className="label">Parent Email</label><input name="parent_email" type="email" className="input" value={form.parent_email} onChange={handleChange} /></div>
        <button type="submit" disabled={loading} className="btn-primary w-full">{loading ? 'Submitting...' : 'Register'}</button>
      </form>
    </div>
  );
}
