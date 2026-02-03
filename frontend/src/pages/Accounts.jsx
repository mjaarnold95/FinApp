import React, { useState, useEffect } from 'react'
import axios from 'axios'

function Accounts() {
  const [accounts, setAccounts] = useState([])
  const [showForm, setShowForm] = useState(false)

  useEffect(() => {
    fetchAccounts()
  }, [])

  const fetchAccounts = async () => {
    try {
      const response = await axios.get('/api/v1/accounts')
      setAccounts(response.data)
    } catch (error) {
      console.error('Error fetching accounts:', error)
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Accounts</h1>
        <p>Manage your financial accounts</p>
      </div>

      <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
        {showForm ? 'Cancel' : '+ Add Account'}
      </button>

      {showForm && (
        <div className="card" style={{ marginTop: '20px' }}>
          <h2>Add New Account</h2>
          <form>
            <div className="form-group">
              <label>Account Name</label>
              <input type="text" placeholder="e.g., Chase Checking" />
            </div>
            <div className="form-group">
              <label>Account Type</label>
              <select>
                <option value="checking">Checking</option>
                <option value="savings">Savings</option>
                <option value="credit_card">Credit Card</option>
                <option value="investment">Investment</option>
                <option value="loan">Loan</option>
              </select>
            </div>
            <div className="form-group">
              <label>Initial Balance</label>
              <input type="number" step="0.01" placeholder="0.00" />
            </div>
            <button type="submit" className="btn btn-primary">Create Account</button>
          </form>
        </div>
      )}

      <div className="card" style={{ marginTop: '20px' }}>
        <h2>Your Accounts</h2>
        {accounts.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Account Name</th>
                <th>Type</th>
                <th>Balance</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {accounts.map(account => (
                <tr key={account.id}>
                  <td>{account.name}</td>
                  <td>{account.account_type}</td>
                  <td>${parseFloat(account.balance).toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
                  <td>{account.is_active ? '✓ Active' : '✗ Inactive'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <div className="icon">🏦</div>
            <h3>No accounts yet</h3>
            <p>Add your first account to get started</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Accounts
