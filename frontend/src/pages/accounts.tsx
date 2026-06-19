import React, { useEffect, useState, useCallback } from 'react';
import { useApiClient } from '@/lib/api';

interface Account {
  id: string;
  name: string;
  type: string;
  balance: number;
  created_at: string;
}

export default function Accounts() {
  const api = useApiClient();
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newAccount, setNewAccount] = useState({ name: '', type: 'asset' });

  const fetchAccounts = useCallback(async () => {
    try {
      setLoading(true);
      const response = await api.get('/accounts');
      setAccounts(response.data || []);
      setError(null);
    } catch (err) {
      setError('Failed to load accounts');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [api]);

  useEffect(() => {
    fetchAccounts();
  }, [fetchAccounts]);

  const handleCreateAccount = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/accounts', newAccount);
      setNewAccount({ name: '', type: 'asset' });
      await fetchAccounts();
    } catch (err) {
      setError('Failed to create account');
      console.error(err);
    }
  };

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
          <p className="text-xs uppercase tracking-[0.2em] text-teal-700 font-semibold mb-2">
            Ledgers
          </p>
          <h1 className="text-4xl font-bold text-slate-900">Accounts</h1>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl mb-6">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1 fade-up-delay" style={{ animationDelay: '60ms' }}>
            <div className="bg-white/90 border border-slate-100 rounded-2xl shadow-sm p-6 transition hover:shadow-md">
              <h2 className="text-xl font-semibold mb-4 text-slate-900">Create Account</h2>
              <form onSubmit={handleCreateAccount} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700">
                    Account Name
                  </label>
                  <input
                    type="text"
                    value={newAccount.name}
                    onChange={(e) =>
                      setNewAccount({ ...newAccount, name: e.target.value })
                    }
                    className="mt-1 block w-full border-slate-300 rounded-lg px-3 py-2 border focus:border-teal-600 focus:outline-none"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700">
                    Account Type
                  </label>
                  <select
                    value={newAccount.type}
                    onChange={(e) =>
                      setNewAccount({ ...newAccount, type: e.target.value })
                    }
                    className="mt-1 block w-full border-slate-300 rounded-lg px-3 py-2 border focus:border-teal-600 focus:outline-none"
                  >
                    <option value="asset">Asset</option>
                    <option value="liability">Liability</option>
                    <option value="equity">Equity</option>
                    <option value="revenue">Revenue</option>
                    <option value="expense">Expense</option>
                  </select>
                </div>
                <button
                  type="submit"
                  className="w-full bg-teal-700 text-white py-2.5 rounded-lg hover:bg-teal-800 transition"
                >
                  Create Account
                </button>
              </form>
            </div>
          </div>

          <div className="lg:col-span-2 fade-up-delay" style={{ animationDelay: '130ms' }}>
            <div className="bg-white/90 border border-slate-100 rounded-2xl shadow-sm transition hover:shadow-md">
              <div className="px-6 py-4 border-b">
                <h2 className="text-xl font-semibold text-slate-900">Your Accounts</h2>
              </div>

              {loading ? (
                <div className="p-6 text-center">
                  <p className="text-slate-600">Loading accounts...</p>
                </div>
              ) : accounts.length === 0 ? (
                <div className="p-6 text-center">
                  <p className="text-slate-600">No accounts found. Create one to get started.</p>
                </div>
              ) : (
                <>
                  <div className="md:hidden space-y-3 p-4">
                    {accounts.map((account, index) => (
                      <article
                        key={account.id}
                        className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm fade-up"
                        style={{ animationDelay: `${index * 45}ms` }}
                      >
                        <div className="flex items-start justify-between gap-3">
                          <h3 className="font-semibold text-slate-900">{account.name}</h3>
                          <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-teal-50 text-teal-800 border border-teal-100">
                            {account.type}
                          </span>
                        </div>
                        <p className="text-sm text-slate-600 mt-2">Balance: ${account.balance.toFixed(2)}</p>
                        <p className="text-xs text-slate-500 mt-1">
                          Opened {new Date(account.created_at).toLocaleDateString()}
                        </p>
                        <div className="mt-3 flex gap-2">
                          <button
                            type="button"
                            onClick={() => copyToClipboard(account.id)}
                            className="px-2.5 py-1.5 text-xs font-medium rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
                          >
                            Copy ID
                          </button>
                          <button
                            type="button"
                            onClick={() => copyToClipboard(account.name)}
                            className="px-2.5 py-1.5 text-xs font-medium rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
                          >
                            Copy Name
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
                          Name
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 uppercase tracking-[0.12em]">
                          Type
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 uppercase tracking-[0.12em]">
                          Balance
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 uppercase tracking-[0.12em]">
                          Created
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-slate-600 uppercase tracking-[0.12em]">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y">
                      {accounts.map((account, index) => (
                        <tr key={account.id} className={index % 2 === 0 ? 'bg-white/70' : 'bg-slate-50/60'}>
                          <td className="px-6 py-4">{account.name}</td>
                          <td className="px-6 py-4">
                            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-teal-50 text-teal-800 border border-teal-100">
                              {account.type}
                            </span>
                          </td>
                          <td className="px-6 py-4 font-semibold">
                            ${account.balance.toFixed(2)}
                          </td>
                          <td className="px-6 py-4 text-sm text-slate-600">
                            {new Date(account.created_at).toLocaleDateString()}
                          </td>
                          <td className="px-6 py-4">
                            <div className="flex items-center gap-2">
                              <button
                                type="button"
                                onClick={() => copyToClipboard(account.id)}
                                className="px-2.5 py-1.5 text-xs font-medium rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
                              >
                                Copy ID
                              </button>
                              <button
                                type="button"
                                onClick={() => copyToClipboard(account.name)}
                                className="px-2.5 py-1.5 text-xs font-medium rounded-md border border-slate-300 text-slate-700 hover:bg-slate-50"
                              >
                                Copy Name
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
      </div>
    </div>
  );
}
