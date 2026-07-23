import { Suspense } from 'react';
import ApplyContent from './ApplyContent';

export default function ApplyPage() {
  return (
    <Suspense fallback={<p className="p-16 text-center">Loading...</p>}>
      <ApplyContent />
    </Suspense>
  );
}
