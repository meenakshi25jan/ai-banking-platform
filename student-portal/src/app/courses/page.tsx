'use client';

import { useEffect, useState } from 'react';
import { api, Course } from '@/lib/api';
import { BookOpen, Clock, Users, IndianRupee } from 'lucide-react';
import Link from 'next/link';

export default function CoursesPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getCourses().then((res) => {
      if (res.status === 'success' && res.data) setCourses(res.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  return (
    <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
      <h1 className="text-4xl font-bold">Our Courses</h1>
      <p className="mt-3 text-gray-600 dark:text-gray-400">Explore programs and check seat availability.</p>

      {loading ? (
        <p className="mt-12 text-center text-gray-500">Loading courses...</p>
      ) : courses.length === 0 ? (
        <p className="mt-12 text-center text-gray-500">No courses available. Please check back later.</p>
      ) : (
        <div className="mt-12 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {courses.map((c) => (
            <div key={c.id} className="card flex flex-col">
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-xs font-medium text-brand-600">{c.code}</span>
                  <h3 className="mt-1 text-lg font-semibold">{c.name}</h3>
                  <p className="text-sm text-gray-500">{c.department} &middot; {c.campus}</p>
                </div>
                <BookOpen className="text-brand-400" size={28} />
              </div>
              <div className="mt-4 flex flex-wrap gap-3 text-sm text-gray-600 dark:text-gray-400">
                <span className="flex items-center gap-1"><Clock size={14} /> {c.duration_months} months</span>
                <span className="flex items-center gap-1"><Users size={14} /> {c.available_seats} seats</span>
                <span className="flex items-center gap-1"><IndianRupee size={14} /> {(c.admission_fee + c.course_fee).toLocaleString()}</span>
              </div>
              {c.eligibility_criteria && (
                <p className="mt-3 text-xs text-gray-500 line-clamp-2">{c.eligibility_criteria}</p>
              )}
              <Link href={`/apply?course=${c.id}`} className="btn-primary mt-auto pt-4 text-center">
                Apply Now
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
