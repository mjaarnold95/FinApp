# FinApp 💰

A comprehensive personal finance application for tracking expenses, income, investments, taxes, payroll, and retirement planning with modern double-entry accounting. Available on **Web, iOS, and macOS** with real-time synchronization.

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
- **🆕 Plaid Integration**: Automatic bank account linking and transaction import
- **🆕 Import/Export**: CSV import and export for transactions, accounts, and investments
- **🆕 Native Apps**: iOS and macOS apps with real-time sync across all platforms
- **🆕 Cross-Platform Sync**: WebSocket-based synchronization ensures data consistency

## Platforms

### Web Application
- Modern React 18 frontend
- Responsive design for desktop and mobile browsers
- Progressive Web App (PWA) support

### iOS Application
- Native SwiftUI app for iPhone and iPad
- iOS 16.0 or later
- Optimized for touch interactions

### macOS Application
- Native SwiftUI app for Mac
- macOS 13.0 (Ventura) or later
- Full keyboard navigation and window management

**All platforms sync in real-time** - changes made on one device instantly appear on all others.

## Tech Stack

### Backend
- **Python** >= 3.14
- **FastAPI** - Modern, fast web framework
- **SQLModel** - SQL database ORM with Pydantic integration
- **PostgreSQL 18** - Database (via psycopg >= 3.3)
- **Plaid** - Bank account integration for automatic transaction import
- **WebSocket** - Real-time synchronization across platforms
- **Uvicorn** - ASGI server
- **uv** - Fast Python package manager

### Frontend
- **React** 18 - Modern UI library
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Vite** - Fast build tool
- **CSS3** - Custom styling with gradients and animations

### Native Apps (iOS & macOS)
- **SwiftUI** - Modern declarative UI framework
- **Combine** - Reactive programming
- **URLSession** - Networking and WebSocket support
- **Universal Binary** - Single codebase for iOS and macOS

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
│   │   │   ├── retirement.py
│   │   │   └── plaid.py
│   │   ├── api/             # API endpoints
│   │   │   ├── users.py
│   │   │   ├── accounts.py
│   │   │   ├── transactions.py
│   │   │   ├── investments.py
│   │   │   ├── payroll.py
│   │   │   ├── retirement.py
│   │   │   ├── taxes.py
│   │   │   ├── plaid.py
│   │   │   ├── import_export.py
│   │   │   └── websocket.py    # Real-time sync
│   │   ├── services/        # Business logic
│   │   │   └── plaid_service.py
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
├── ios-macos/               # Native iOS & macOS apps
│   ├── FinApp.xcodeproj/    # Xcode project
│   ├── FinApp/
│   │   ├── FinAppApp.swift  # App entry point
│   │   ├── Models/          # Data models
│   │   │   └── Models.swift
│   │   ├── Views/           # SwiftUI views
│   │   │   ├── ContentView.swift
│   │   │   ├── DashboardView.swift
│   │   │   ├── AccountsView.swift
│   │   │   └── TransactionsView.swift
│   │   └── Services/        # API & sync services
│   │       ├── APIService.swift
│   │       └── SyncService.swift
│   └── README.md
└── README.md
```

## Installation

### Prerequisites
- Python >= 3.14
- Node.js >= 18
- PostgreSQL >= 18
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

### iOS & macOS Apps Setup

1. Navigate to the iOS/macOS directory:
```bash
cd ios-macos
```

2. Open the project in Xcode:
```bash
open FinApp.xcodeproj
```

3. Select your target:
   - **FinApp-iOS** for iPhone/iPad simulator or device
   - **FinApp-macOS** for Mac

4. Build and run (⌘R)

**Note**: The apps connect to `http://localhost:8000` by default. Make sure the backend is running before launching the native apps.

For more details, see [ios-macos/README.md](ios-macos/README.md)

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

### 🆕 Plaid Integration
- `POST /api/v1/plaid/link-token` - Create Plaid Link token for bank connection
- `POST /api/v1/plaid/exchange-token` - Exchange public token and link accounts
- `POST /api/v1/plaid/sync-transactions` - Sync transactions from linked bank
- `GET /api/v1/plaid/items` - List linked bank connections
- `DELETE /api/v1/plaid/items/{id}` - Remove bank connection

### 🆕 Import/Export
- `POST /api/v1/import-export/transactions/import` - Import transactions from CSV
- `GET /api/v1/import-export/transactions/export` - Export transactions to CSV
- `POST /api/v1/import-export/accounts/import` - Import accounts from CSV
- `GET /api/v1/import-export/accounts/export` - Export accounts to CSV
- `POST /api/v1/import-export/investments/import` - Import investments from CSV
- `GET /api/v1/import-export/investments/export` - Export investments to CSV

## Plaid Integration

FinApp integrates with Plaid to automatically import transactions from your bank accounts.

### Setup
1. Sign up for a Plaid account at https://plaid.com
2. Get your Client ID and Secret from the Plaid Dashboard
3. Add them to your `.env` file:
   ```
   PLAID_CLIENT_ID=your-client-id
   PLAID_SECRET=your-secret
   PLAID_ENVIRONMENT=sandbox  # Use 'production' for real banks
   ```

### Usage
1. Call `POST /api/v1/plaid/link-token` to get a link token
2. Use Plaid Link (frontend) to connect a bank account
3. Exchange the public token with `POST /api/v1/plaid/exchange-token`
4. Sync transactions with `POST /api/v1/plaid/sync-transactions`

Transactions are automatically imported and ledger entries are created following double-entry accounting principles.

## Import/Export

### CSV Import Format

**Transactions CSV:**
```csv
date,description,amount,category,merchant,account_id
2024-01-15,Grocery Store,75.50,Food & Dining,Whole Foods,1
2024-01-16,Salary,2500.00,Income,Employer,2
```

**Accounts CSV:**
```csv
name,account_type,balance,currency
Chase Checking,checking,5000.00,USD
Savings Account,savings,10000.00,USD
```

**Investments CSV:**
```csv
symbol,name,investment_type,quantity,purchase_price,current_price,purchase_date,account_id
AAPL,Apple Inc.,stock,10,150.00,175.00,2024-01-01,1
TSLA,Tesla Inc.,stock,5,200.00,220.00,2024-01-15,1
```

## Cross-Platform Synchronization

FinApp keeps your data in sync across all platforms in real-time using WebSocket technology.

### How It Works

1. **WebSocket Connection**: Each app (web, iOS, macOS) establishes a WebSocket connection to the backend at `ws://localhost:8000/ws/sync/{user_id}`

2. **Real-Time Updates**: When data changes on any platform:
   - The backend broadcasts a notification to all connected clients for that user
   - All other apps receive the notification and refresh their data
   - Changes appear instantly across all devices

3. **Fallback Polling**: If WebSocket is unavailable:
   - Apps poll the server every 30 seconds for changes
   - Ensures synchronization even with network issues

### Example Sync Flow

```
User adds transaction on iOS
    ↓
iOS app → POST /api/v1/transactions
    ↓
Backend creates transaction & ledger entries
    ↓
Backend broadcasts WebSocket message
    ↓
macOS app ← WebSocket notification
Web app ← WebSocket notification
    ↓
All apps refresh and display new transaction
```

### Running Multiple Apps

1. Start the backend server:
   ```bash
   cd backend
   python run.py
   ```

2. Start the web app:
   ```bash
   cd frontend
   npm run dev
   ```

3. Open the iOS/macOS app in Xcode and run

All apps will automatically sync changes made in any of them.

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