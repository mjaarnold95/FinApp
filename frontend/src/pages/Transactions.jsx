import React, { useState, useEffect } from 'react'
import axios from 'axios'

function Transactions() {
  const [transactions, setTransactions] = useState([])

  useEffect(() => {
    fetchTransactions()
  }, [])

  const fetchTransactions = async () => {
    try {
      const response = await axios.get('/api/v1/transactions')
      setTransactions(response.data)
    } catch (error) {
      console.error('Error fetching transactions:', error)
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Transactions</h1>
        <p>Track your income and expenses</p>
      </div>

      <button className="btn btn-primary">+ Add Transaction</button>

      <div className="card" style={{ marginTop: '20px' }}>
        <h2>Transaction History</h2>
        {transactions.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Description</th>
                <th>Category</th>
                <th>Amount</th>
                <th>Account</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map(transaction => (
                <tr key={transaction.id}>
                  <td>{new Date(transaction.transaction_date).toLocaleDateString()}</td>
                  <td>{transaction.description}</td>
                  <td>{transaction.category || 'Uncategorized'}</td>
                  <td style={{ color: transaction.amount >= 0 ? '#48bb78' : '#f56565' }}>
                    ${Math.abs(parseFloat(transaction.amount)).toLocaleString('en-US', { minimumFractionDigits: 2 })}
                  </td>
                  <td>Account #{transaction.account_id}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <div className="icon">💳</div>
            <h3>No transactions yet</h3>
            <p>Add your first transaction to start tracking</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Transactions
