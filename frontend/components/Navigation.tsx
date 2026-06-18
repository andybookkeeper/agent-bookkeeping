import React from 'react';
import Link from 'next/link';
import styles from '../styles/navigation.module.css';

export default function Navigation() {
  return (
    <nav className={styles.nav}>
      <Link href="/" className={styles.navLink}>
        Dashboard
      </Link>
      <Link href="/accounts" className={styles.navLink}>
        Accounts
      </Link>
      <Link href="/transactions" className={styles.navLink}>
        Transactions
      </Link>
      <Link href="/invoices" className={styles.navLink}>
        Invoices
      </Link>
      <Link href="/payments" className={styles.navLink}>
        Payments
      </Link>
      <Link href="/receipts" className={styles.navLink}>
        Receipts
      </Link>
    </nav>
  );
}
