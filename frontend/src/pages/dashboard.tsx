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
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {loading ? (
          <div className="text-center py-12">
            <p className="text-gray-600">Loading dashboard data...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-gray-500 text-sm font-medium">Total Accounts</div>
              <div className="text-3xl font-bold text-gray-900 mt-2">
                {stats.totalAccounts}
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-gray-500 text-sm font-medium">Transactions</div>
              <div className="text-3xl font-bold text-gray-900 mt-2">
                {stats.totalTransactions}
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-gray-500 text-sm font-medium">Invoices</div>
              <div className="text-3xl font-bold text-gray-900 mt-2">
                {stats.totalInvoices}
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-gray-500 text-sm font-medium">Total Balance</div>
              <div className="text-3xl font-bold text-gray-900 mt-2">
                ${stats.totalBalance.toFixed(2)}
              </div>
            </div>
          </div>
        )}

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Quick Links</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <Link href="/accounts" className="text-blue-600 hover:text-blue-700">
              → Manage Accounts
            </Link>
            <Link href="/transactions" className="text-blue-600 hover:text-blue-700">
              → View Transactions
            </Link>
            <Link href="/invoices" className="text-blue-600 hover:text-blue-700">
              → Create Invoice
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
