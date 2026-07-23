'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { GraduationCap, Menu, X } from 'lucide-react';
import { useState } from 'react';
import { ThemeToggle } from './ThemeToggle';
import { useAuth } from '@/lib/auth';
import clsx from 'clsx';

const links = [
  { href: '/', label: 'Home' },
  { href: '/about', label: 'About' },
  { href: '/courses', label: 'Courses' },
  { href: '/register', label: 'Register' },
  { href: '/apply', label: 'Apply' },
  { href: '/contact', label: 'Contact' },
];

export function Navbar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-gray-200 bg-white/80 backdrop-blur-md dark:border-gray-800 dark:bg-gray-950/80">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <Link href="/" className="flex items-center gap-2 font-bold text-brand-700 dark:text-brand-400">
          <GraduationCap size={28} />
          <span className="hidden sm:inline">Student Admission ERP</span>
        </Link>

        <div className="hidden items-center gap-1 md:flex">
          {links.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className={clsx(
                'rounded-lg px-3 py-2 text-sm font-medium transition',
                pathname === l.href
                  ? 'bg-brand-50 text-brand-700 dark:bg-brand-900/30 dark:text-brand-300'
                  : 'text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800',
              )}
            >
              {l.label}
            </Link>
          ))}
        </div>

        <div className="flex items-center gap-2">
          <ThemeToggle />
          {user ? (
            <>
              <Link href="/dashboard" className="btn-secondary hidden sm:inline-flex">Dashboard</Link>
              <button onClick={() => logout()} className="btn-secondary text-sm">Logout</button>
            </>
          ) : (
            <Link href="/login" className="btn-primary">Login</Link>
          )}
          <button className="rounded-lg p-2 md:hidden" onClick={() => setOpen(!open)}>
            {open ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>
      </nav>

      {open && (
        <div className="border-t border-gray-200 px-4 py-3 md:hidden dark:border-gray-800">
          {links.map((l) => (
            <Link key={l.href} href={l.href} onClick={() => setOpen(false)}
              className="block rounded-lg px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300">
              {l.label}
            </Link>
          ))}
        </div>
      )}
    </header>
  );
}
