import React, { useState, useEffect } from 'react'
import axios from 'axios'

function Investments() {
  const [investments, setInvestments] = useState([])

  useEffect(() => {
    fetchInvestments()
  }, [])

  const fetchInvestments = async () => {
    try {
      const response = await axios.get('/api/v1/investments')
      setInvestments(response.data)
    } catch (error) {
      console.error('Error fetching investments:', error)
    }
  }

  const calculateGainLoss = (investment) => {
    const currentValue = parseFloat(investment.current_price) * parseFloat(investment.quantity)
    const purchaseValue = parseFloat(investment.purchase_price) * parseFloat(investment.quantity)
    return currentValue - purchaseValue
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Investments</h1>
        <p>Track your investment portfolio</p>
      </div>

      <button className="btn btn-primary">+ Add Investment</button>

      <div className="card" style={{ marginTop: '20px' }}>
        <h2>Portfolio</h2>
        {investments.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Symbol</th>
                <th>Name</th>
                <th>Type</th>
                <th>Quantity</th>
                <th>Purchase Price</th>
                <th>Current Price</th>
                <th>Gain/Loss</th>
              </tr>
            </thead>
            <tbody>
              {investments.map(investment => {
                const gainLoss = calculateGainLoss(investment)
                return (
                  <tr key={investment.id}>
                    <td><strong>{investment.symbol}</strong></td>
                    <td>{investment.name}</td>
                    <td>{investment.investment_type}</td>
                    <td>{parseFloat(investment.quantity).toFixed(2)}</td>
                    <td>${parseFloat(investment.purchase_price).toFixed(2)}</td>
                    <td>${parseFloat(investment.current_price).toFixed(2)}</td>
                    <td style={{ color: gainLoss >= 0 ? '#48bb78' : '#f56565' }}>
                      ${Math.abs(gainLoss).toLocaleString('en-US', { minimumFractionDigits: 2 })}
                      {gainLoss >= 0 ? ' ↑' : ' ↓'}
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <div className="icon">📈</div>
            <h3>No investments yet</h3>
            <p>Add your first investment to start tracking your portfolio</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Investments
