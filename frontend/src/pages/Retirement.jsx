import React, { useState, useEffect } from 'react'
import axios from 'axios'

function Retirement() {
  const [retirementAccounts, setRetirementAccounts] = useState([])

  useEffect(() => {
    fetchRetirementAccounts()
  }, [])

  const fetchRetirementAccounts = async () => {
    try {
      const response = await axios.get('/api/v1/retirement')
      setRetirementAccounts(response.data)
    } catch (error) {
      console.error('Error fetching retirement accounts:', error)
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Retirement</h1>
        <p>Plan for your future with retirement accounts</p>
      </div>

      <button className="btn btn-primary">+ Add Retirement Account</button>

      <div className="card" style={{ marginTop: '20px' }}>
        <h2>Retirement Accounts</h2>
        {retirementAccounts.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Account Name</th>
                <th>Type</th>
                <th>Balance</th>
                <th>Contribution Limit</th>
                <th>YTD Contributions</th>
                <th>Employer Match</th>
              </tr>
            </thead>
            <tbody>
              {retirementAccounts.map(account => (
                <tr key={account.id}>
                  <td>{account.account_name}</td>
                  <td>{account.retirement_type.replace('_', ' ').toUpperCase()}</td>
                  <td>${parseFloat(account.balance).toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
                  <td>${parseFloat(account.contribution_limit).toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
                  <td>${parseFloat(account.year_to_date_contribution).toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
                  <td>{account.employer_match_percent ? `${account.employer_match_percent}%` : 'N/A'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <div className="icon">🏖️</div>
            <h3>No retirement accounts yet</h3>
            <p>Add your first retirement account to start planning for the future</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Retirement
