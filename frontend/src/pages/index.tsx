import React from 'react';
import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Bookkeeping Platform
          </h1>
          <p className="text-xl text-gray-600">
            Professional accounting and financial management system
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Link href="/dashboard">
            <div className="p-6 bg-white rounded-lg shadow hover:shadow-lg transition cursor-pointer">
              <h2 className="text-xl font-semibold mb-2">Dashboard</h2>
              <p className="text-gray-600">View financial overview and analytics</p>
            </div>
          </Link>

          <Link href="/accounts">
            <div className="p-6 bg-white rounded-lg shadow hover:shadow-lg transition cursor-pointer">
              <h2 className="text-xl font-semibold mb-2">Accounts</h2>
              <p className="text-gray-600">Manage chart of accounts</p>
            </div>
          </Link>

          <Link href="/transactions">
            <div className="p-6 bg-white rounded-lg shadow hover:shadow-lg transition cursor-pointer">
              <h2 className="text-xl font-semibold mb-2">Transactions</h2>
              <p className="text-gray-600">Record and review transactions</p>
            </div>
          </Link>

          <Link href="/journal-entries">
            <div className="p-6 bg-white rounded-lg shadow hover:shadow-lg transition cursor-pointer">
              <h2 className="text-xl font-semibold mb-2">Journal Entries</h2>
              <p className="text-gray-600">Double-entry accounting records</p>
            </div>
          </Link>

          <Link href="/invoices">
            <div className="p-6 bg-white rounded-lg shadow hover:shadow-lg transition cursor-pointer">
              <h2 className="text-xl font-semibold mb-2">Invoices</h2>
              <p className="text-gray-600">Create and manage invoices</p>
            </div>
          </Link>

          <Link href="/receipts">
            <div className="p-6 bg-white rounded-lg shadow hover:shadow-lg transition cursor-pointer">
              <h2 className="text-xl font-semibold mb-2">Receipts</h2>
              <p className="text-gray-600">Upload and organize receipts</p>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
}
