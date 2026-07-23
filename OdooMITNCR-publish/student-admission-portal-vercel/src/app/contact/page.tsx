'use client';
import { useState } from 'react';
import { api } from '@/lib/api';
import { Mail, Phone, MapPin, CheckCircle } from 'lucide-react';

export default function ContactPage() {
  const [form, setForm] = useState({ name: '', email: '', message: '' });
  const [sent, setSent] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.sendContact(form);
    setSent(true);
  };

  if (sent) return (
    <div className="mx-auto max-w-lg px-4 py-20 text-center">
      <CheckCircle className="mx-auto text-green-500" size={64} />
      <h1 className="mt-6 text-3xl font-bold">Message Sent!</h1>
    </div>
  );

  return (
    <div className="mx-auto max-w-4xl px-4 py-16">
      <h1 className="text-4xl font-bold">Contact Us</h1>
      <div className="mt-12 grid gap-8 md:grid-cols-2">
        <div className="space-y-4">
          <p className="flex items-center gap-3"><Mail className="text-brand-600" size={20} /> admissions@institute.edu</p>
          <p className="flex items-center gap-3"><Phone className="text-brand-600" size={20} /> +91 22 1234 5678</p>
          <p className="flex items-center gap-3"><MapPin className="text-brand-600" size={20} /> 123 University Road, Mumbai</p>
        </div>
        <form onSubmit={submit} className="card space-y-4">
          <div><label className="label">Name</label><input required className="input" value={form.name} onChange={e => setForm({...form, name: e.target.value})} /></div>
          <div><label className="label">Email</label><input type="email" required className="input" value={form.email} onChange={e => setForm({...form, email: e.target.value})} /></div>
          <div><label className="label">Message</label><textarea required className="input" rows={4} value={form.message} onChange={e => setForm({...form, message: e.target.value})} /></div>
          <button type="submit" className="btn-primary w-full">Send Message</button>
        </form>
      </div>
    </div>
  );
}
