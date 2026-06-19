import React, { useEffect, useState, useCallback } from 'react';
import Link from 'next/link';
import { useApiClient } from '@/lib/api';

interface DashboardStats {
  totalAccounts: number;
  totalTransactions: number;
  totalInvoices: number;
  totalBalance: number;
}

export default function Dashboard() {
  const api = useApiClient();
  const [stats, setStats] = useState<DashboardStats>({
    totalAccounts: 0,
    totalTransactions: 0,
    totalInvoices: 0,
    totalBalance: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = useCallback(async () => {
    try {
      setLoading(true);
      const [accountsRes, transactionsRes, invoicesRes] = await Promise.all([
        api.get('/accounts?limit=1'),
        api.get('/transactions?limit=1'),
        api.get('/invoices?limit=1'),
      ]);

      setStats({
        totalAccounts: accountsRes.data?.length || 0,
        totalTransactions: transactionsRes.data?.length || 0,
        totalInvoices: invoicesRes.data?.length || 0,
        totalBalance: 0,
      });
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [api]);

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  return (
    <div className="max-w-7xl mx-auto">
      <div className="glass-panel rounded-3xl p-6 md:p-8 fade-up">
        <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mb-7">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-teal-700 font-semibold mb-2">
              Operations
            </p>
            <h1 className="text-4xl font-bold text-slate-900">Dashboard</h1>
          </div>
          <p className="text-sm text-slate-600">Live snapshot of your bookkeeping activity.</p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl mb-6">
            {error}
          </div>
        )}

        {loading ? (
          <div className="text-center py-12">
            <p className="text-slate-600">Loading dashboard data...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <div className="bg-white/90 border border-slate-100 p-6 rounded-2xl shadow-sm">
              <div className="text-slate-500 text-xs uppercase tracking-[0.16em] font-semibold">Total Accounts</div>
              <div className="text-3xl font-bold text-slate-900 mt-2">
                {stats.totalAccounts}
              </div>
            </div>

            <div className="bg-white/90 border border-slate-100 p-6 rounded-2xl shadow-sm">
              <div className="text-slate-500 text-xs uppercase tracking-[0.16em] font-semibold">Transactions</div>
              <div className="text-3xl font-bold text-slate-900 mt-2">
                {stats.totalTransactions}
              </div>
            </div>

            <div className="bg-white/90 border border-slate-100 p-6 rounded-2xl shadow-sm">
              <div className="text-slate-500 text-xs uppercase tracking-[0.16em] font-semibold">Invoices</div>
              <div className="text-3xl font-bold text-slate-900 mt-2">
                {stats.totalInvoices}
              </div>
            </div>

            <div className="bg-white/90 border border-slate-100 p-6 rounded-2xl shadow-sm">
              <div className="text-slate-500 text-xs uppercase tracking-[0.16em] font-semibold">Total Balance</div>
              <div className="text-3xl font-bold text-slate-900 mt-2">
                ${stats.totalBalance.toFixed(2)}
              </div>
            </div>
          </div>
        )}

        <div className="bg-white/90 border border-slate-100 rounded-2xl shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4 text-slate-900">Quick Links</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <Link href="/accounts" className="text-teal-700 hover:text-teal-800 font-medium">
              → Manage Accounts
            </Link>
            <Link href="/transactions" className="text-teal-700 hover:text-teal-800 font-medium">
              → View Transactions
            </Link>
            <Link href="/invoices" className="text-teal-700 hover:text-teal-800 font-medium">
              → Create Invoice
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
