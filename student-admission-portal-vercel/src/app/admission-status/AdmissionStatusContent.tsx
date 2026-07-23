'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { api, AdmissionDetail } from '@/lib/api';

const STEPS = ['draft','submitted','under_review','verified','approved','admitted'];

export default function AdmissionStatusContent() {
  const params = useSearchParams();
  const id = Number(params.get('id'));
  const [data, setData] = useState<AdmissionDetail | null>(null);

  useEffect(() => {
    if (id) api.getAdmission(id).then(r => r.data && setData(r.data));
  }, [id]);

  if (!data) return <p className="p-16 text-center">Loading...</p>;
  const stepIdx = STEPS.indexOf(data.state);

  return (
    <div className="mx-auto max-w-3xl px-4 py-16">
      <h1 className="text-3xl font-bold">Admission Status</h1>
      <p className="mt-1 text-gray-600">{data.admission_number} — {data.student_name}</p>
      <div className="mt-8 flex justify-between">
        {STEPS.map((s, i) => (
          <div key={s} className="flex flex-col items-center text-center">
            <div className={`h-8 w-8 rounded-full text-xs flex items-center justify-center font-bold ${i <= stepIdx ? 'bg-brand-600 text-white' : 'bg-gray-200 text-gray-500'}`}>{i+1}</div>
            <span className="mt-1 hidden text-xs sm:block capitalize">{s.replace('_',' ')}</span>
          </div>
        ))}
      </div>
      <div className="mt-8 grid gap-4 sm:grid-cols-3">
        <div className="card"><p className="text-sm text-gray-500">Course</p><p className="font-semibold">{data.course}</p></div>
        <div className="card"><p className="text-sm text-gray-500">Department</p><p className="font-semibold">{data.department}</p></div>
        <div className="card"><p className="text-sm text-gray-500">Status</p><p className="font-semibold capitalize">{data.state.replace('_',' ')}</p></div>
      </div>
      {data.documents && (
        <div className="mt-8"><h2 className="font-semibold">Documents</h2>
          <ul className="mt-3 space-y-2">{data.documents.map(d => (
            <li key={d.id} className="flex justify-between rounded-lg border p-3 text-sm">
              <span>{d.name}</span><span className="capitalize">{d.state}</span>
            </li>
          ))}</ul>
        </div>
      )}
      {data.fees && (
        <div className="mt-8"><h2 className="font-semibold">Fees</h2>
          <ul className="mt-3 space-y-2">{data.fees.map(f => (
            <li key={f.id} className="flex justify-between rounded-lg border p-3 text-sm">
              <span>{f.fee_type} — {f.receipt_number}</span><span>₹{f.amount} ({f.state})</span>
            </li>
          ))}</ul>
        </div>
      )}
    </div>
  );
}
