import React, { useEffect, useState, useCallback } from 'react';
import { useApiClient } from '@/lib/api';

interface Transaction {
  id: string;
  date: string;
  description: string;
  amount: number;
  source: string;
  status: string;
}

export default function Transactions() {
  const api = useApiClient();
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState('');

  const fetchTransactions = useCallback(async () => {
    try {
      setLoading(true);
      const params = statusFilter ? `?status=${statusFilter}` : '';
      const response = await api.get(`/transactions${params}`);
      setTransactions(response.data || []);
      setError(null);
    } catch (err) {
      setError('Failed to load transactions');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [api, statusFilter]);

  useEffect(() => {
    fetchTransactions();
  }, [fetchTransactions]);

  const copyToClipboard = async (value: string) => {
    try {
      await navigator.clipboard.writeText(value);
    } catch (err) {
      console.error(err);
      setError('Unable to copy to clipboard');
    }
  };

  return (
    <div className="max-w-7xl mx-auto">
      <div className="glass-panel rounded-3xl p-6 md:p-8 fade-up">
        <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mb-7">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-teal-700 font-semibold mb-2">Flow</p>
            <h1 className="text-4xl font-bold text-slate-900">Transactions</h1>
          </div>
          <p className="text-sm text-slate-600">Filter by processing status for quick triage.</p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl mb-6">
            {error}
          </div>
        )}

        <div className="bg-white/90 border border-slate-100 rounded-2xl shadow-sm fade-up-delay" style={{ animationDelay: '90ms' }}>
          <div className="px-6 py-4 border-b flex justify-between items-center">
            <h2 className="text-xl font-semibold text-slate-900">Recent Transactions</h2>
            <div>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="border-slate-300 rounded-lg px-3 py-2 border focus:border-teal-600 focus:outline-none"
              >
                <option value="">All Status</option>
                <option value="pending">Pending</option>
                <option value="processing">Processing</option>
                <option value="completed">Completed</option>
                <option value="failed">Failed</option>
              </select>
            </div>
          </div>

          {loading ? (
            <div className="p-6 text-center">
              <p className="text-slate-600">Loading transactions...</p>
            </div>
          ) : transactions.length === 0 ? (
            <div className="p-6 text-center">
              <p className="text-slate-600">No transactions found.</p>
            </div>
          ) : (
            <>
              <div className="md:hidden space-y-3 p-4">
                {transactions.map((transaction, index) => (
                  <article
                    key={transaction.id}
                    className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm fade-up"
                    style={{ animationDelay: `${index * 40}ms` }}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <p className="font-semibold text-slate-900">{transaction.description}</p>
                      <span
                        className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border ${
                          transaction.status === 'completed'
                            ? 'bg-emerald-50 text-emerald-700 border-emerald-100'
                            : transaction.status === 'pending'
                            ? 'bg-amber-50 text-amber-700 border-amber-100'
                            : transaction.status === 'failed'
                            ? 'bg-red-50 text-red-700 border-red-100'
                            : 'bg-slate-100 text-slate-700 border-slate-200'
                        }`}
                      >
                        {transaction.status}
                      </span>
                    </div>
                    <p className="text-sm text-slate-600 mt-2">
                      {new Date(transaction.date).toLocaleDateString()} • {transaction.source}
                    </p>
                    <p className="text-base font-semibold text-slate-900 mt-1">${transaction.amount.toFixed(2)}</p>
                    <div className="mt-3 flex gap-2">
                      <button
                        type="button"
                        onClick={() => copyToClipboard(transaction.id)}
                        className="px-2.5 py-1.5 text-xs font-medium rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
                      >
                        Copy ID
                      </button>
                      <button
                        type="button"
                        onClick={() => copyToClipboard(transaction.description)}
                        className="px-2.5 py-1.5 text-xs font-medium rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
                      >
                        Copy Memo
                      </button>
                    </div>
                  </article>
                ))}
              </div>

              <div className="hidden md:block overflow-x-auto max-h-[30rem]">
                <table className="w-full">
                  <thead className="bg-slate-50 border-b sticky top-0 z-10">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 uppercase tracking-[0.12em]">
                      Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 uppercase tracking-[0.12em]">
                      Description
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 uppercase tracking-[0.12em]">
                      Amount
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 uppercase tracking-[0.12em]">
                      Source
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 uppercase tracking-[0.12em]">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 uppercase tracking-[0.12em]">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {transactions.map((transaction, index) => (
                    <tr key={transaction.id} className={index % 2 === 0 ? 'bg-white/70' : 'bg-slate-50/60'}>
                      <td className="px-6 py-4">
                        {new Date(transaction.date).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4">{transaction.description}</td>
                      <td className="px-6 py-4 font-semibold">
                        ${transaction.amount.toFixed(2)}
                      </td>
                      <td className="px-6 py-4">{transaction.source}</td>
                      <td className="px-6 py-4">
                        <span
                          className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border ${
                            transaction.status === 'completed'
                              ? 'bg-emerald-50 text-emerald-700 border-emerald-100'
                              : transaction.status === 'pending'
                              ? 'bg-amber-50 text-amber-700 border-amber-100'
                              : transaction.status === 'failed'
                              ? 'bg-red-50 text-red-700 border-red-100'
                              : 'bg-slate-100 text-slate-700 border-slate-200'
                          }`}
                        >
                          {transaction.status}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <button
                            type="button"
                            onClick={() => copyToClipboard(transaction.id)}
                            className="px-2.5 py-1.5 text-xs font-medium rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
                          >
                            Copy ID
                          </button>
                          <button
                            type="button"
                            onClick={() => copyToClipboard(transaction.description)}
                            className="px-2.5 py-1.5 text-xs font-medium rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
                          >
                            Copy Memo
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
