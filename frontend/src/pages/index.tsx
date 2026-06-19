import React from 'react';
import Link from 'next/link';

export default function Home() {
  const cards = [
    {
      href: '/dashboard',
      title: 'Mission Control',
      desc: 'Live operational view of accounts, transactions, and invoice activity.',
    },
    {
      href: '/accounts',
      title: 'Account Architect',
      desc: 'Build and tune your chart of accounts with strict categorization.',
    },
    {
      href: '/transactions',
      title: 'Flow Monitor',
      desc: 'Track incoming records and status transitions in one place.',
    },
    {
      href: '/invoices',
      title: 'Billing Desk',
      desc: 'Review invoice lifecycle and maintain collection cadence.',
    },
    {
      href: '/receipts',
      title: 'Receipt Vault',
      desc: 'Keep receipts searchable and paired with transaction evidence.',
    },
  ];

  return (
    <div className="max-w-7xl mx-auto">
      <section className="glass-panel rounded-3xl p-8 md:p-12 fade-up">
        <div className="max-w-3xl">
          <p className="text-xs tracking-[0.22em] uppercase text-teal-700 font-semibold mb-4">
            Browser Workspace
          </p>
          <h1 className="text-4xl md:text-6xl font-bold text-slate-900 leading-tight mb-5">
            Accounting with signal, not noise.
          </h1>
          <p className="text-lg text-slate-600 mb-7">
            LedgerCraft gives your finance operations a clear cockpit: strict posting rules,
            searchable records, and workflows designed for speed.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link
              href="/dashboard"
              className="px-5 py-2.5 rounded-full bg-teal-700 text-white font-semibold hover:bg-teal-800 transition"
            >
              Open Dashboard
            </Link>
            <Link
              href="/accounts"
              className="px-5 py-2.5 rounded-full border border-teal-700 text-teal-800 font-semibold hover:bg-teal-50 transition"
            >
              Configure Accounts
            </Link>
          </div>
        </div>
      </section>

      <section className="mt-8 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5 fade-up-delay">
        {cards.map((card) => (
          <Link
            key={card.href}
            href={card.href}
            className="glass-panel rounded-2xl p-6 hover:-translate-y-1 hover:shadow-xl transition"
          >
            <h2 className="text-xl font-semibold text-slate-900 mb-2">{card.title}</h2>
            <p className="text-slate-600 text-sm leading-relaxed">{card.desc}</p>
          </Link>
        ))}
      </section>

      <section className="mt-8 glass-panel rounded-3xl p-6 md:p-8">
        <h3 className="text-2xl font-semibold text-slate-900 mb-3">What changed</h3>
        <p className="text-slate-600 leading-relaxed">
          This interface is now purpose-built for browser operations: persistent navigation,
          high-contrast controls, and a clean hierarchy that keeps financial actions obvious.
        </p>
      </section>
        </div>
  );
}
