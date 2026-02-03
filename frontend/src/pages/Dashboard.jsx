import React, { useState, useEffect } from 'react'
import axios from 'axios'

function Dashboard() {
  const [stats, setStats] = useState({
    totalBalance: 0,
    monthlyIncome: 0,
    monthlyExpenses: 0,
    investmentValue: 0
  })

  useEffect(() => {
    // Fetch dashboard stats
    // This would call the API endpoints to aggregate data
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      // Example: fetch accounts and calculate total balance
      const accountsRes = await axios.get('/api/v1/accounts')
      const totalBalance = accountsRes.data.reduce((sum, acc) => sum + parseFloat(acc.balance), 0)
      
      setStats(prev => ({
        ...prev,
        totalBalance
      }))
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Dashboard</h1>
        <p>Welcome to your financial overview</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Balance</h3>
          <div className="value">${stats.totalBalance.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>
          <div className="change positive">↑ 5.2% from last month</div>
        </div>

        <div className="stat-card">
          <h3>Monthly Income</h3>
          <div className="value">${stats.monthlyIncome.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>
          <div className="change positive">↑ 2.1% from last month</div>
        </div>

        <div className="stat-card">
          <h3>Monthly Expenses</h3>
          <div className="value">${stats.monthlyExpenses.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>
          <div className="change negative">↓ 3.5% from last month</div>
        </div>

        <div className="stat-card">
          <h3>Investment Value</h3>
          <div className="value">${stats.investmentValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>
          <div className="change positive">↑ 8.7% from last month</div>
        </div>
      </div>

      <div className="card">
        <h2>Recent Transactions</h2>
        <div className="empty-state">
          <div className="icon">💳</div>
          <h3>No recent transactions</h3>
          <p>Your recent transactions will appear here</p>
        </div>
      </div>

      <div className="card">
        <h2>Financial Insights</h2>
        <div className="empty-state">
          <div className="icon">📊</div>
          <h3>Insights coming soon</h3>
          <p>AI-powered insights about your finances will appear here</p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
