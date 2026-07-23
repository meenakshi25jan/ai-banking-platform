import Link from 'next/link';
import { GraduationCap, Mail, Phone, MapPin } from 'lucide-react';

export function Footer() {
  return (
    <footer className="border-t border-gray-200 bg-gray-50 dark:border-gray-800 dark:bg-gray-900">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid gap-8 md:grid-cols-3">
          <div>
            <div className="flex items-center gap-2 font-bold text-brand-700 dark:text-brand-400">
              <GraduationCap size={24} />
              Student Admission ERP
            </div>
            <p className="mt-3 text-sm text-gray-600 dark:text-gray-400">
              Complete institution management for schools, colleges, and universities.
            </p>
          </div>
          <div>
            <h3 className="font-semibold">Quick Links</h3>
            <ul className="mt-3 space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <li><Link href="/courses" className="hover:text-brand-600">Courses</Link></li>
              <li><Link href="/register" className="hover:text-brand-600">Register</Link></li>
              <li><Link href="/apply" className="hover:text-brand-600">Apply for Admission</Link></li>
              <li><Link href="/contact" className="hover:text-brand-600">Contact</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold">Contact</h3>
            <ul className="mt-3 space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <li className="flex items-center gap-2"><Mail size={14} /> admissions@institute.edu</li>
              <li className="flex items-center gap-2"><Phone size={14} /> +91 22 1234 5678</li>
              <li className="flex items-center gap-2"><MapPin size={14} /> Mumbai, India</li>
            </ul>
          </div>
        </div>
        <div className="mt-8 border-t border-gray-200 pt-6 text-center text-sm text-gray-500 dark:border-gray-700">
          &copy; {new Date().getFullYear()} Student Admission ERP. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
