import React from 'react';
import Layout from '../components/Layout';

export default function Dashboard() {
  return (
    <Layout>
      <h1>Dashboard</h1>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <div style={{ border: '1px solid #ccc', padding: '20px' }}>
          <h2>Total Accounts</h2>
          <p style={{ fontSize: '24px', fontWeight: 'bold' }}>--</p>
        </div>
        <div style={{ border: '1px solid #ccc', padding: '20px' }}>
          <h2>Total Balance</h2>
          <p style={{ fontSize: '24px', fontWeight: 'bold' }}>$--</p>
        </div>
        <div style={{ border: '1px solid #ccc', padding: '20px' }}>
          <h2>Recent Transactions</h2>
          <p>No transactions yet</p>
        </div>
        <div style={{ border: '1px solid #ccc', padding: '20px' }}>
          <h2>Pending Invoices</h2>
          <p>No pending invoices</p>
        </div>
      </div>
    </Layout>
  );
}
