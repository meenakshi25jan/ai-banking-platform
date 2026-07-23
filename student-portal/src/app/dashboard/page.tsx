'use client';
import { useEffect, useState } from 'react';
import { useAuth } from '@/lib/auth';
import { api, DashboardData, Admission } from '@/lib/api';
import { Users, FileText, CheckCircle, XCircle, IndianRupee, Clock } from 'lucide-react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function DashboardPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [dash, setDash] = useState<DashboardData | null>(null);
  const [admissions, setAdmissions] = useState<Admission[]>([]);

  useEffect(() => {
    if (!authLoading && !user) router.push('/login');
  }, [user, authLoading, router]);

  useEffect(() => {
    if (user) {
      api.getDashboard().then(r => r.data && setDash(r.data));
      api.getAdmissions().then(r => r.data && setAdmissions(r.data));
    }
  }, [user]);

  if (authLoading || !user) return <p className="p-16 text-center">Loading...</p>;

  const cards = dash ? [
    { label: 'Total Students', value: dash.total_students, icon: Users, color: 'text-blue-600' },
    { label: 'Pending', value: dash.pending_admissions, icon: Clock, color: 'text-yellow-600' },
    { label: 'Approved', value: dash.approved_admissions, icon: CheckCircle, color: 'text-green-600' },
    { label: 'Rejected', value: dash.rejected_admissions, icon: XCircle, color: 'text-red-600' },
    { label: 'Fee Collected', value: `₹${dash.fee_collected.toLocaleString()}`, icon: IndianRupee, color: 'text-emerald-600' },
    { label: 'Applications', value: dash.total_applications, icon: FileText, color: 'text-purple-600' },
  ] : [];

  return (
    <div className="mx-auto max-w-7xl px-4 py-16">
      <h1 className="text-3xl font-bold">Welcome, {user.name}</h1>
      <p className="mt-1 text-gray-600">Student Dashboard</p>
      <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {cards.map(c => (
          <div key={c.label} className="card flex items-center gap-4">
            <c.icon className={c.color} size={32} />
            <div><p className="text-2xl font-bold">{c.value}</p><p className="text-sm text-gray-500">{c.label}</p></div>
          </div>
        ))}
      </div>
      <h2 className="mt-12 text-xl font-semibold">My Applications</h2>
      <div className="mt-4 overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead><tr className="border-b"><th className="p-3">Admission No.</th><th className="p-3">Course</th><th className="p-3">Status</th><th className="p-3">Pending Fee</th><th className="p-3"></th></tr></thead>
          <tbody>
            {admissions.map(a => (
              <tr key={a.id} className="border-b">
                <td className="p-3">{a.admission_number}</td>
                <td className="p-3">{a.course}</td>
                <td className="p-3"><span className="rounded-full bg-brand-100 px-2 py-1 text-xs font-medium text-brand-700">{a.state}</span></td>
                <td className="p-3">₹{a.pending_fee?.toLocaleString()}</td>
                <td className="p-3"><Link href={`/admission-status?id=${a.id}`} className="text-brand-600 hover:underline">View</Link></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
