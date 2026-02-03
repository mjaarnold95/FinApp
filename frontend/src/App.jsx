import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Accounts from './pages/Accounts'
import Transactions from './pages/Transactions'
import Investments from './pages/Investments'
import Payroll from './pages/Payroll'
import Retirement from './pages/Retirement'
import Taxes from './pages/Taxes'
import './styles/App.css'

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)

  return (
    <Router>
      <div className="app">
        <nav className={`sidebar ${isSidebarOpen ? 'open' : 'closed'}`}>
          <div className="sidebar-header">
            <h1>💰 FinApp</h1>
            <button 
              className="toggle-btn"
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            >
              {isSidebarOpen ? '←' : '→'}
            </button>
          </div>
          {isSidebarOpen && (
            <ul className="nav-links">
              <li><Link to="/">📊 Dashboard</Link></li>
              <li><Link to="/accounts">🏦 Accounts</Link></li>
              <li><Link to="/transactions">💳 Transactions</Link></li>
              <li><Link to="/investments">📈 Investments</Link></li>
              <li><Link to="/payroll">💼 Payroll</Link></li>
              <li><Link to="/retirement">🏖️ Retirement</Link></li>
              <li><Link to="/taxes">📋 Taxes</Link></li>
            </ul>
          )}
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/accounts" element={<Accounts />} />
            <Route path="/transactions" element={<Transactions />} />
            <Route path="/investments" element={<Investments />} />
            <Route path="/payroll" element={<Payroll />} />
            <Route path="/retirement" element={<Retirement />} />
            <Route path="/taxes" element={<Taxes />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
