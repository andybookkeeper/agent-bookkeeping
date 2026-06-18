import React from 'react';
import Layout from '../components/Layout';
import AccountsList from '../components/AccountsList';

export default function AccountsPage() {
  return (
    <Layout>
      <h1>Accounts</h1>
      <AccountsList />
    </Layout>
  );
}
