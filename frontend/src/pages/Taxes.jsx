import React, { useState, useEffect } from 'react'
import axios from 'axios'

function Taxes() {
  const [taxRecords, setTaxRecords] = useState([])

  useEffect(() => {
    fetchTaxRecords()
  }, [])

  const fetchTaxRecords = async () => {
    try {
      const response = await axios.get('/api/v1/taxes')
      setTaxRecords(response.data)
    } catch (error) {
      console.error('Error fetching tax records:', error)
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Taxes</h1>
        <p>Manage your tax information and records</p>
      </div>

      <button className="btn btn-primary">+ Add Tax Record</button>

      <div className="card" style={{ marginTop: '20px' }}>
        <h2>Tax Records</h2>
        {taxRecords.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Tax Year</th>
                <th>Filing Status</th>
                <th>Gross Income</th>
                <th>Taxable Income</th>
                <th>Total Tax</th>
                <th>Refund/Owed</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {taxRecords.map(record => (
                <tr key={record.id}>
                  <td>{record.tax_year}</td>
                  <td>{record.filing_status.replace('_', ' ')}</td>
                  <td>${parseFloat(record.gross_income).toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
                  <td>${parseFloat(record.taxable_income).toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
                  <td>${parseFloat(record.total_tax).toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
                  <td style={{ color: record.refund_or_owed >= 0 ? '#48bb78' : '#f56565' }}>
                    ${Math.abs(parseFloat(record.refund_or_owed)).toLocaleString('en-US', { minimumFractionDigits: 2 })}
                    {record.refund_or_owed >= 0 ? ' (Refund)' : ' (Owed)'}
                  </td>
                  <td>{record.filing_date ? '✓ Filed' : '⏳ Pending'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <div className="icon">📋</div>
            <h3>No tax records yet</h3>
            <p>Add your first tax record to track filings and obligations</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Taxes
