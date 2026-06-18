import React from 'react';
import Link from 'next/link';
import styles from '../styles/layout.module.css';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className={styles.container}>
      <nav className={styles.navbar}>
        <div className={styles.logo}>
          <Link href="/">Agent Bookkeeping</Link>
        </div>
        <ul className={styles.navLinks}>
          <li>
            <Link href="/">Dashboard</Link>
          </li>
          <li>
            <Link href="/accounts">Accounts</Link>
          </li>
          <li>
            <Link href="/transactions">Transactions</Link>
          </li>
          <li>
            <Link href="/invoices">Invoices</Link>
          </li>
          <li>
            <Link href="/payments">Payments</Link>
          </li>
          <li>
            <Link href="/receipts">Receipts</Link>
          </li>
        </ul>
      </nav>
      <main className={styles.main}>{children}</main>
      <footer className={styles.footer}>
        <p>&copy; 2024 Agent Bookkeeping Platform. All rights reserved.</p>
      </footer>
    </div>
  );
}
