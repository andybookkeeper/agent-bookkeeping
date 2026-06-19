import type { AppProps } from 'next/app';
import Link from 'next/link';
import { useRouter } from 'next/router';
import './globals.css';

export default function App({ Component, pageProps }: AppProps) {
  const router = useRouter();

  const links = [
    { href: '/', label: 'Home' },
    { href: '/dashboard', label: 'Dashboard' },
    { href: '/accounts', label: 'Accounts' },
    { href: '/transactions', label: 'Transactions' },
    { href: '/invoices', label: 'Invoices' },
    { href: '/receipts', label: 'Receipts' },
  ];

  return (
    <div className="flex flex-col min-h-screen">
      <nav className="px-4 pt-4 md:pt-6">
        <div className="max-w-7xl mx-auto">
          <div className="glass-panel rounded-2xl px-4 py-4 md:px-6 md:py-5 fade-up">
            <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
              <Link href="/" className="text-xl md:text-2xl font-bold text-teal-800">
                LedgerCraft
              </Link>
              <div className="flex flex-wrap items-center gap-2 md:justify-end">
                {links.map((link) => {
                  const active = router.pathname === link.href;
                  return (
                    <Link
                      key={link.href}
                      href={link.href}
                      className={`px-3 py-1.5 rounded-full text-sm font-medium transition ${
                        active
                          ? 'bg-teal-700 text-white shadow-sm'
                          : 'bg-white text-slate-700 border border-slate-200 hover:border-teal-500 hover:text-teal-700'
                      }`}
                    >
                      {link.label}
                    </Link>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main className="flex-1 px-4 py-6 md:py-10">
        <Component {...pageProps} />
      </main>

      <footer className="mt-auto px-4 pb-6 md:pb-8">
        <div className="max-w-7xl mx-auto">
          <div className="glass-panel rounded-2xl px-4 py-4 text-center text-sm text-slate-600">
            <p>LedgerCraft • operational bookkeeping in real time</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
