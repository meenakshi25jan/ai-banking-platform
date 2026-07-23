import { Suspense } from 'react';
import AdmissionStatusContent from './AdmissionStatusContent';

export default function AdmissionStatusPage() {
  return (
    <Suspense fallback={<p className="p-16 text-center">Loading...</p>}>
      <AdmissionStatusContent />
    </Suspense>
  );
}
