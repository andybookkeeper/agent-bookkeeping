import React, { useEffect, useState } from 'react';
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

  useEffect(() => {
    fetchInvoices();
  }, []);

  const fetchInvoices = async () => {
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
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Invoices</h1>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b">
            <h2 className="text-xl font-semibold">Your Invoices</h2>
          </div>

          {loading ? (
            <div className="p-6 text-center">
              <p className="text-gray-600">Loading invoices...</p>
            </div>
          ) : invoices.length === 0 ? (
            <div className="p-6 text-center">
              <p className="text-gray-600">No invoices found.</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-700">
                      Invoice ID
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-700">
                      Amount
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-700">
                      Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-700">
                      Due Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-700">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {invoices.map((invoice) => (
                    <tr key={invoice.id} className="hover:bg-gray-50">
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
                          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            invoice.status === 'paid'
                              ? 'bg-green-100 text-green-800'
                              : invoice.status === 'sent'
                              ? 'bg-blue-100 text-blue-800'
                              : invoice.status === 'draft'
                              ? 'bg-gray-100 text-gray-800'
                              : 'bg-red-100 text-red-800'
                          }`}
                        >
                          {invoice.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
