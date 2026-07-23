import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

export async function GET() {
  const odooUrl = process.env.NEXT_PUBLIC_ODOO_URL || 'http://localhost:8069';
  let odooStatus = 'unknown';

  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);
    const res = await fetch(`${odooUrl}/api/health`, {
      signal: controller.signal,
      cache: 'no-store',
    });
    clearTimeout(timeout);
    odooStatus = res.ok ? 'ok' : `error:${res.status}`;
  } catch {
    odooStatus = 'unreachable';
  }

  const healthy = true;

  return NextResponse.json(
    {
      status: healthy ? 'ok' : 'degraded',
      service: 'student-admission-portal',
      timestamp: new Date().toISOString(),
      odoo: {
        url: odooUrl,
        status: odooStatus,
      },
    },
    { status: 200 },
  );
}
