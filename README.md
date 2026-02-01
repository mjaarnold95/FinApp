# FinApp 💰

A comprehensive personal finance application for tracking expenses, income, investments, taxes, payroll, and retirement planning with modern double-entry accounting.

## Features

- **User Management**: Secure user authentication and profile management
- **Financial Institutions**: Track banks, credit unions, and brokerages
- **Accounts**: Manage checking, savings, credit cards, investments, loans, and more
- **Transactions**: Record income and expenses with detailed categorization
- **Double-Entry Ledger**: Proper accounting with debits and credits
- **Investments**: Track stocks, bonds, ETFs, crypto, and real estate
- **Taxes**: Manage tax records, withholdings, and filings
- **Payroll**: Track jobs, deductions, and withholdings
- **Retirement**: Plan for retirement with 401(k), IRA, and pension accounts
- **Financial Insights**: Dashboard with comprehensive financial overview

## Tech Stack

### Backend
- **Python** >= 3.14
- **FastAPI** - Modern, fast web framework
- **SQLModel** - SQL database ORM with Pydantic integration
- **PostgreSQL** - Database (via psycopg >= 3.3)
- **Uvicorn** - ASGI server
- **uv** - Fast Python package manager

### Frontend
- **React** 18 - Modern UI library
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Vite** - Fast build tool
- **CSS3** - Custom styling with gradients and animations

## Project Structure

```
FinApp/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   │   ├── user.py
│   │   │   ├── account.py
│   │   │   ├── transaction.py
│   │   │   ├── ledger.py
│   │   │   ├── investment.py
│   │   │   ├── tax.py
│   │   │   ├── payroll.py
│   │   │   └── retirement.py
│   │   ├── api/             # API endpoints
│   │   │   ├── users.py
│   │   │   ├── accounts.py
│   │   │   ├── transactions.py
│   │   │   ├── investments.py
│   │   │   ├── payroll.py
│   │   │   ├── retirement.py
│   │   │   └── taxes.py
│   │   ├── core/            # Core configuration
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   └── main.py          # FastAPI application
│   ├── run.py               # Server runner
│   └── pyproject.toml       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── pages/           # Page components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Accounts.jsx
│   │   │   ├── Transactions.jsx
│   │   │   ├── Investments.jsx
│   │   │   ├── Payroll.jsx
│   │   │   ├── Retirement.jsx
│   │   │   └── Taxes.jsx
│   │   ├── styles/          # CSS styles
│   │   ├── App.jsx          # Main app component
│   │   └── main.jsx         # Entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Installation

### Prerequisites
- Python >= 3.14
- Node.js >= 18
- PostgreSQL >= 14
- uv (Python package manager)

### Backend Setup

1. Install uv if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Navigate to the backend directory:
```bash
cd backend
```

3. Create a virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

4. Set up environment variables (create `.env` file):
```env
DATABASE_URL=postgresql://finapp:finapp@localhost:5432/finapp
SECRET_KEY=your-secret-key-change-in-production
```

5. Set up PostgreSQL database:
```bash
# Create database and user
psql -U postgres
CREATE DATABASE finapp;
CREATE USER finapp WITH PASSWORD 'finapp';
GRANT ALL PRIVILEGES ON DATABASE finapp TO finapp;
```

6. Run the backend server:
```bash
python run.py
```

The API will be available at http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## API Documentation

The API provides comprehensive endpoints for managing all financial data:

### Users
- `GET /api/v1/users` - List all users
- `GET /api/v1/users/{id}` - Get user details
- `POST /api/v1/users` - Create user
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

### Accounts
- `GET /api/v1/accounts` - List accounts
- `GET /api/v1/accounts/{id}` - Get account details
- `POST /api/v1/accounts` - Create account
- `PUT /api/v1/accounts/{id}` - Update account
- `DELETE /api/v1/accounts/{id}` - Delete account

### Transactions
- `GET /api/v1/transactions` - List transactions
- `GET /api/v1/transactions/{id}` - Get transaction details
- `POST /api/v1/transactions` - Create transaction (auto-creates ledger entries)
- `DELETE /api/v1/transactions/{id}` - Delete transaction

### Investments
- `GET /api/v1/investments` - List investments
- `GET /api/v1/investments/{id}` - Get investment details
- `POST /api/v1/investments` - Create investment
- `PUT /api/v1/investments/{id}` - Update investment
- `DELETE /api/v1/investments/{id}` - Delete investment

### Payroll
- `GET /api/v1/payroll` - List payroll records
- `GET /api/v1/payroll/{id}` - Get payroll details
- `POST /api/v1/payroll` - Create payroll record
- `GET /api/v1/payroll/{id}/deductions` - Get deductions
- `POST /api/v1/payroll/{id}/deductions` - Add deduction
- `GET /api/v1/payroll/{id}/withholdings` - Get withholdings
- `POST /api/v1/payroll/{id}/withholdings` - Add withholding

### Retirement
- `GET /api/v1/retirement` - List retirement accounts
- `GET /api/v1/retirement/{id}` - Get retirement account details
- `POST /api/v1/retirement` - Create retirement account
- `PUT /api/v1/retirement/{id}` - Update retirement account
- `DELETE /api/v1/retirement/{id}` - Delete retirement account

### Taxes
- `GET /api/v1/taxes` - List tax records
- `GET /api/v1/taxes/{id}` - Get tax record details
- `POST /api/v1/taxes` - Create tax record
- `PUT /api/v1/taxes/{id}` - Update tax record
- `DELETE /api/v1/taxes/{id}` - Delete tax record

## Database Models

### Double-Entry Accounting
The application implements proper double-entry accounting through the `LedgerEntry` model. Every transaction creates corresponding ledger entries with debits and credits, ensuring accurate financial tracking.

### Account Types
- **Asset Accounts**: Checking, Savings, Investment
- **Liability Accounts**: Credit Card, Loan
- **Equity Accounts**: Owner's equity
- **Revenue Accounts**: Income sources
- **Expense Accounts**: Spending categories

## Development

### Running Tests
```bash
cd backend
uv pip install pytest httpx
pytest
```

### Building for Production

#### Backend
```bash
cd backend
uv pip install -e .
```

#### Frontend
```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please open an issue on GitHub.