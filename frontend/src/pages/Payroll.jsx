import React, { useState, useEffect } from 'react'
import axios from 'axios'

function Payroll() {
  const [payrollRecords, setPayrollRecords] = useState([])

  useEffect(() => {
    fetchPayrollRecords()
  }, [])

  const fetchPayrollRecords = async () => {
    try {
      const response = await axios.get('/api/v1/payroll')
      setPayrollRecords(response.data)
    } catch (error) {
      console.error('Error fetching payroll records:', error)
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Payroll</h1>
        <p>Manage jobs, deductions, and withholdings</p>
      </div>

      <button className="btn btn-primary">+ Add Payroll Record</button>

      <div className="card" style={{ marginTop: '20px' }}>
        <h2>Payroll Records</h2>
        {payrollRecords.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Employer</th>
                <th>Job Title</th>
                <th>Pay Date</th>
                <th>Gross Pay</th>
                <th>Net Pay</th>
                <th>YTD Gross</th>
              </tr>
            </thead>
            <tbody>
              {payrollRecords.map(record => (
                <tr key={record.id}>
                  <td>{record.employer_name}</td>
                  <td>{record.job_title}</td>
                  <td>{new Date(record.pay_date).toLocaleDateString()}</td>
                  <td>${parseFloat(record.gross_pay).toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
                  <td>${parseFloat(record.net_pay).toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
                  <td>${parseFloat(record.year_to_date_gross).toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <div className="icon">💼</div>
            <h3>No payroll records yet</h3>
            <p>Add your first payroll record to track income and deductions</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Payroll
