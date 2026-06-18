import type { AppProps } from 'next/app';
import Link from 'next/link';
import './globals.css';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <div className="flex flex-col min-h-screen">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <Link href="/" className="text-xl font-bold text-blue-600">
              Bookkeeping
            </Link>
            <div className="flex gap-6">
              <Link href="/" className="text-gray-600 hover:text-gray-900">
                Home
              </Link>
              <Link href="/dashboard" className="text-gray-600 hover:text-gray-900">
                Dashboard
              </Link>
              <Link href="/accounts" className="text-gray-600 hover:text-gray-900">
                Accounts
              </Link>
              <Link href="/transactions" className="text-gray-600 hover:text-gray-900">
                Transactions
              </Link>
              <Link href="/invoices" className="text-gray-600 hover:text-gray-900">
                Invoices
              </Link>
              <Link href="/receipts" className="text-gray-600 hover:text-gray-900">
                Receipts
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="flex-1">
        <Component {...pageProps} />
      </main>

      <footer className="bg-gray-900 text-white mt-auto">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center">
          <p>&copy; 2024 Agent Bookkeeping Platform. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
