import React from 'react';
import Layout from '../components/Layout';
import TransactionForm from '../components/TransactionForm';

export default function TransactionsPage() {
  return (
    <Layout>
      <h1>Transactions</h1>
      <TransactionForm />
    </Layout>
  );
}
