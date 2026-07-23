import Link from 'next/link';
import { ArrowRight, BookOpen, Users, Award, FileCheck } from 'lucide-react';

const features = [
  { icon: BookOpen, title: 'Online Registration', desc: 'Register online with document upload and instant confirmation.' },
  { icon: FileCheck, title: 'Admission Tracking', desc: 'Track your application from submission to admission in real-time.' },
  { icon: Award, title: 'Merit & Scholarships', desc: 'Merit-based evaluation with scholarship and discount support.' },
  { icon: Users, title: 'Student Portal', desc: 'Access fees, documents, and admission status from one dashboard.' },
];

export default function HomePage() {
  return (
    <>
      <section className="relative overflow-hidden bg-gradient-to-br from-brand-600 via-brand-700 to-brand-900 text-white">
        <div className="mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8">
          <div className="max-w-2xl">
            <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl lg:text-6xl">
              Your Future Starts Here
            </h1>
            <p className="mt-6 text-lg text-brand-100">
              Register, apply, and track your admission journey online.
              Built for schools, colleges, universities, and training institutes.
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Link href="/register" className="inline-flex items-center gap-2 rounded-lg bg-white px-6 py-3 font-semibold text-brand-700 shadow-lg transition hover:bg-brand-50">
                Register Now <ArrowRight size={18} />
              </Link>
              <Link href="/courses" className="inline-flex items-center gap-2 rounded-lg border-2 border-white/30 px-6 py-3 font-semibold text-white transition hover:bg-white/10">
                Browse Courses
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
        <h2 className="text-center text-3xl font-bold">Why Choose Us</h2>
        <p className="mx-auto mt-3 max-w-2xl text-center text-gray-600 dark:text-gray-400">
          A complete digital admission experience powered by Odoo ERP.
        </p>
        <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((f) => (
            <div key={f.title} className="card text-center">
              <f.icon className="mx-auto text-brand-600" size={36} />
              <h3 className="mt-4 font-semibold">{f.title}</h3>
              <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="bg-gray-50 py-20 dark:bg-gray-900">
        <div className="mx-auto max-w-7xl px-4 text-center sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold">Ready to Apply?</h2>
          <p className="mt-3 text-gray-600 dark:text-gray-400">Start your admission journey in minutes.</p>
          <Link href="/apply" className="btn-primary mt-6 inline-flex gap-2">
            Apply for Admission <ArrowRight size={18} />
          </Link>
        </div>
      </section>
    </>
  );
}
