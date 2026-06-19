import React, { useEffect, useState, useCallback } from 'react';
import { useApiClient } from '@/lib/api';

interface Invoice {
  id: string;
  amount: number;
  date: string;
  due_date: string;
  status: string;
  account_id: string;
}

export default function Invoices() {
  const api = useApiClient();
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchInvoices = useCallback(async () => {
    try {
      setLoading(true);
      const response = await api.get('/invoices');
      setInvoices(response.data || []);
      setError(null);
    } catch (err) {
      setError('Failed to load invoices');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [api]);

  useEffect(() => {
    fetchInvoices();
  }, [fetchInvoices]);

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
        <div className="mb-7">
          <p className="text-xs uppercase tracking-[0.2em] text-teal-700 font-semibold mb-2">Billing</p>
          <h1 className="text-4xl font-bold text-slate-900">Invoices</h1>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl mb-6">
            {error}
          </div>
        )}

        <div className="bg-white/90 border border-slate-100 rounded-2xl shadow-sm fade-up-delay" style={{ animationDelay: '90ms' }}>
          <div className="px-6 py-4 border-b">
            <h2 className="text-xl font-semibold text-slate-900">Your Invoices</h2>
          </div>

          {loading ? (
            <div className="p-6 text-center">
              <p className="text-slate-600">Loading invoices...</p>
            </div>
          ) : invoices.length === 0 ? (
            <div className="p-6 text-center">
              <p className="text-slate-600">No invoices found.</p>
            </div>
          ) : (
            <>
              <div className="md:hidden space-y-3 p-4">
                {invoices.map((invoice, index) => (
                  <article
                    key={invoice.id}
                    className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm fade-up"
                    style={{ animationDelay: `${index * 40}ms` }}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <p className="font-semibold text-slate-900">{invoice.id.slice(0, 8)}...</p>
                      <span
                        className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border ${
                          invoice.status === 'paid'
                            ? 'bg-emerald-50 text-emerald-700 border-emerald-100'
                            : invoice.status === 'sent'
                            ? 'bg-sky-50 text-sky-700 border-sky-100'
                            : invoice.status === 'draft'
                            ? 'bg-slate-100 text-slate-700 border-slate-200'
                            : 'bg-red-50 text-red-700 border-red-100'
                        }`}
                      >
                        {invoice.status}
                      </span>
                    </div>
                    <p className="text-base font-semibold text-slate-900 mt-2">${invoice.amount.toFixed(2)}</p>
                    <p className="text-sm text-slate-600 mt-1">
                      {new Date(invoice.date).toLocaleDateString()} • due {new Date(invoice.due_date).toLocaleDateString()}
                    </p>
                    <div className="mt-3 flex gap-2">
                      <button
                        type="button"
                        onClick={() => copyToClipboard(invoice.id)}
                        className="px-2.5 py-1.5 text-xs font-medium rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
                      >
                        Copy ID
                      </button>
                      <button
                        type="button"
                        onClick={() => copyToClipboard(invoice.account_id)}
                        className="px-2.5 py-1.5 text-xs font-medium rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
                      >
                        Copy Account
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
                      Invoice ID
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 uppercase tracking-[0.12em]">
                      Amount
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 uppercase tracking-[0.12em]">
                      Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 uppercase tracking-[0.12em]">
                      Due Date
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
                  {invoices.map((invoice, index) => (
                    <tr key={invoice.id} className={index % 2 === 0 ? 'bg-white/70' : 'bg-slate-50/60'}>
                      <td className="px-6 py-4 text-sm">{invoice.id.slice(0, 8)}...</td>
                      <td className="px-6 py-4 font-semibold">
                        ${invoice.amount.toFixed(2)}
                      </td>
                      <td className="px-6 py-4">
                        {new Date(invoice.date).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4">
                        {new Date(invoice.due_date).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4">
                        <span
                          className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border ${
                            invoice.status === 'paid'
                              ? 'bg-emerald-50 text-emerald-700 border-emerald-100'
                              : invoice.status === 'sent'
                              ? 'bg-sky-50 text-sky-700 border-sky-100'
                              : invoice.status === 'draft'
                              ? 'bg-slate-100 text-slate-700 border-slate-200'
                              : 'bg-red-50 text-red-700 border-red-100'
                          }`}
                        >
                          {invoice.status}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <button
                            type="button"
                            onClick={() => copyToClipboard(invoice.id)}
                            className="px-2.5 py-1.5 text-xs font-medium rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
                          >
                            Copy ID
                          </button>
                          <button
                            type="button"
                            onClick={() => copyToClipboard(invoice.account_id)}
                            className="px-2.5 py-1.5 text-xs font-medium rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
                          >
                            Copy Account
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
