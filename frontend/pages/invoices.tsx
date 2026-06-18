import React from 'react';
import Layout from '../components/Layout';
import InvoiceTable from '../components/InvoiceTable';

export default function InvoicesPage() {
  return (
    <Layout>
      <h1>Invoices</h1>
      <InvoiceTable />
    </Layout>
  );
}
