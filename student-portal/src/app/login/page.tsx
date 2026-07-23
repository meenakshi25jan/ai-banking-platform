'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';

export default function LoginPage() {
  const { login } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true); setError('');
    const res = await login(email, password);
    if (res.success) router.push('/dashboard');
    else setError(res.message || 'Invalid credentials');
    setLoading(false);
  };

  return (
    <div className="mx-auto flex min-h-[60vh] max-w-md items-center px-4 py-16">
      <div className="w-full">
        <h1 className="text-3xl font-bold">Student Login</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">Access your admission dashboard</p>
        {error && <p className="mt-4 rounded-lg bg-red-50 p-3 text-sm text-red-600">{error}</p>}
        <form onSubmit={handleSubmit} className="mt-8 space-y-4">
          <div><label className="label">Email</label>
            <input type="email" required className="input" value={email} onChange={e => setEmail(e.target.value)} /></div>
          <div><label className="label">Password</label>
            <input type="password" required className="input" value={password} onChange={e => setPassword(e.target.value)} /></div>
          <button type="submit" disabled={loading} className="btn-primary w-full">{loading ? 'Signing in...' : 'Sign In'}</button>
        </form>
      </div>
    </div>
  );
}
