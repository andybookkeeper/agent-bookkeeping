import React, { useEffect, useState, useCallback } from 'react';
import { useApiClient } from '@/lib/api';

interface Receipt {
  id: string;
  transaction_id: string;
  file_path: string;
  uploaded_at: string;
}

export default function Receipts() {
  const api = useApiClient();
  const [receipts, setReceipts] = useState<Receipt[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchReceipts = useCallback(async () => {
    try {
      setLoading(true);
      const response = await api.get('/receipts');
      setReceipts(response.data || []);
      setError(null);
    } catch (err) {
      setError('Failed to load receipts');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [api]);

  useEffect(() => {
    fetchReceipts();
  }, [fetchReceipts]);

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
          <p className="text-xs uppercase tracking-[0.2em] text-teal-700 font-semibold mb-2">Evidence</p>
          <h1 className="text-4xl font-bold text-slate-900">Receipts</h1>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl mb-6">
            {error}
          </div>
        )}

        <div className="bg-white/90 border border-slate-100 rounded-2xl shadow-sm fade-up-delay" style={{ animationDelay: '90ms' }}>
          <div className="px-6 py-4 border-b">
            <h2 className="text-xl font-semibold text-slate-900">Uploaded Receipts</h2>
          </div>

          {loading ? (
            <div className="p-6 text-center">
              <p className="text-slate-600">Loading receipts...</p>
            </div>
          ) : receipts.length === 0 ? (
            <div className="p-6 text-center">
              <p className="text-slate-600">No receipts found. Upload your first receipt to get started.</p>
            </div>
          ) : (
            <>
              <div className="md:hidden space-y-3 p-4">
                {receipts.map((receipt, index) => (
                  <article
                    key={receipt.id}
                    className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm fade-up"
                    style={{ animationDelay: `${index * 40}ms` }}
                  >
                    <p className="font-semibold text-slate-900">{receipt.id.slice(0, 8)}...</p>
                    <p className="text-sm text-slate-600 mt-2 break-all">{receipt.file_path}</p>
                    <p className="text-xs text-slate-500 mt-2">
                      Uploaded {new Date(receipt.uploaded_at).toLocaleDateString()}
                    </p>
                    <div className="mt-3 flex gap-2">
                      <button
                        type="button"
                        onClick={() => copyToClipboard(receipt.id)}
                        className="px-2.5 py-1.5 text-xs font-medium rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
                      >
                        Copy ID
                      </button>
                      <button
                        type="button"
                        onClick={() => copyToClipboard(receipt.file_path)}
                        className="px-2.5 py-1.5 text-xs font-medium rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
                      >
                        Copy Path
                      </button>
                      <button
                        type="button"
                        className="px-2.5 py-1.5 text-xs font-medium rounded-md text-teal-700 border border-teal-200 hover:bg-teal-50"
                      >
                        View
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
                      Receipt ID
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 uppercase tracking-[0.12em]">
                      File Path
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 uppercase tracking-[0.12em]">
                      Uploaded
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 uppercase tracking-[0.12em]">
                      Action
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {receipts.map((receipt, index) => (
                    <tr key={receipt.id} className={index % 2 === 0 ? 'bg-white/70' : 'bg-slate-50/60'}>
                      <td className="px-6 py-4 text-sm">{receipt.id.slice(0, 8)}...</td>
                      <td className="px-6 py-4 text-sm truncate max-w-[260px]">{receipt.file_path}</td>
                      <td className="px-6 py-4">
                        {new Date(receipt.uploaded_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <button
                            type="button"
                            onClick={() => copyToClipboard(receipt.id)}
                            className="px-2.5 py-1.5 text-xs font-medium rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
                          >
                            Copy ID
                          </button>
                          <button
                            type="button"
                            onClick={() => copyToClipboard(receipt.file_path)}
                            className="px-2.5 py-1.5 text-xs font-medium rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
                          >
                            Copy Path
                          </button>
                          <button type="button" className="text-teal-700 hover:text-teal-800 text-sm font-medium">
                            View
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
