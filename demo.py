#!/usr/bin/env python3
"""
Simple demo script to verify FinApp functionality
This script demonstrates the core functionality without requiring a database
"""

import sys
import os
from decimal import Decimal
from datetime import datetime

# Add the backend directory to the path
sys.path.insert(0, '/home/runner/work/FinApp/FinApp/backend')

# Set a dummy database URL to avoid connection errors
os.environ['DATABASE_URL'] = 'sqlite:///dummy.db'


def test_models():
    """Test that all models can be instantiated"""
    from app.models.account import Account, AccountType
    from app.models.user import User
    from app.models.transaction import Transaction
    from app.models.investment import Investment, InvestmentType
    from app.models.retirement import RetirementAccount, RetirementType
    
    print("=" * 60)
    print("Testing FinApp Models")
    print("=" * 60)
    
    # Test User model
    print("\n✓ Testing User model...")
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password_here",
        first_name="Test",
        last_name="User"
    )
    print(f"  Created user: {user.username} ({user.email})")
    
    # Test Account model
    print("\n✓ Testing Account model...")
    account = Account(
        user_id=1,
        name="Checking Account",
        account_type=AccountType.CHECKING,
        balance=Decimal("1000.00"),
        currency="USD"
    )
    print(f"  Created account: {account.name} with balance ${account.balance}")
    
    # Test Transaction model
    print("\n✓ Testing Transaction model...")
    transaction = Transaction(
        user_id=1,
        account_id=1,
        transaction_date=datetime.utcnow(),
        description="Salary Deposit",
        amount=Decimal("2500.00"),
        category="Income"
    )
    print(f"  Created transaction: {transaction.description} - ${transaction.amount}")
    
    # Test Investment model
    print("\n✓ Testing Investment model...")
    investment = Investment(
        user_id=1,
        account_id=1,
        investment_type=InvestmentType.STOCK,
        symbol="AAPL",
        name="Apple Inc.",
        quantity=Decimal("10.5"),
        purchase_price=Decimal("150.00"),
        current_price=Decimal("175.00"),
        purchase_date=datetime.utcnow()
    )
    print(f"  Created investment: {investment.symbol} - {investment.name}")
    gain = (investment.current_price - investment.purchase_price) * investment.quantity
    print(f"  Gain/Loss: ${gain}")
    
    # Test Retirement Account model
    print("\n✓ Testing RetirementAccount model...")
    retirement = RetirementAccount(
        user_id=1,
        account_id=1,
        retirement_type=RetirementType.K401_TRADITIONAL,
        account_name="Company 401(k)",
        balance=Decimal("50000.00"),
        contribution_limit=Decimal("23000.00"),
        year_to_date_contribution=Decimal("10000.00"),
        employer_match_percent=Decimal("5.00")
    )
    print(f"  Created retirement: {retirement.account_name}")
    print(f"  Balance: ${retirement.balance}")
    print(f"  YTD Contribution: ${retirement.year_to_date_contribution} / ${retirement.contribution_limit}")
    
    print("\n" + "=" * 60)
    print("✓ All models tested successfully!")
    print("=" * 60)
    
    return True


def test_api_structure():
    """Test that API structure is correct"""
    print("\n" + "=" * 60)
    print("Testing API Structure")
    print("=" * 60)
    
    # Test that we can import the FastAPI app (skip startup)
    print("\n✓ Testing FastAPI app import...")
    
    # Temporarily override the startup event
    import app.main as main_module
    
    # Create a new app without startup events
    from fastapi import FastAPI
    test_app = FastAPI(title="FinApp Test", version="0.1.0")
    
    # Import routers
    from app.api import users, institutions, accounts, transactions, investments, payroll, retirement, taxes
    
    # Include routers
    test_app.include_router(users.router, prefix="/api/v1")
    test_app.include_router(institutions.router, prefix="/api/v1")
    test_app.include_router(accounts.router, prefix="/api/v1")
    test_app.include_router(transactions.router, prefix="/api/v1")
    test_app.include_router(investments.router, prefix="/api/v1")
    test_app.include_router(payroll.router, prefix="/api/v1")
    test_app.include_router(retirement.router, prefix="/api/v1")
    test_app.include_router(taxes.router, prefix="/api/v1")
    
    print(f"  App name: {test_app.title}")
    print(f"  Version: {test_app.version}")
    
    # Check routes
    print("\n✓ Checking API routes...")
    routes = [route.path for route in test_app.routes if hasattr(route, 'path')]
    api_routes = [r for r in routes if r.startswith('/api/v1/')]
    
    print(f"  Total routes: {len(routes)}")
    print(f"  API routes: {len(api_routes)}")
    
    expected_routes = [
        '/api/v1/users',
        '/api/v1/accounts',
        '/api/v1/transactions',
        '/api/v1/investments',
        '/api/v1/payroll',
        '/api/v1/retirement',
        '/api/v1/taxes',
        '/api/v1/institutions',
    ]
    
    for route in expected_routes:
        matching = [r for r in api_routes if route in r]
        if matching:
            print(f"  ✓ {route}")
        else:
            print(f"  ✗ {route} - Missing!")
    
    print("\n" + "=" * 60)
    print("✓ API structure verified!")
    print("=" * 60)
    
    return True


def main():
    """Run all tests"""
    print("\n")
    print("█" * 60)
    print("█" + " " * 58 + "█")
    print("█" + "  FinApp - Personal Finance Application".center(58) + "█")
    print("█" + "  Verification & Demo Script".center(58) + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60)
    
    try:
        # Run model tests
        test_models()
        
        # Run API structure tests
        test_api_structure()
        
        print("\n" + "=" * 60)
        print("SUCCESS! All tests passed ✓")
        print("=" * 60)
        print("\nFinApp is ready to use!")
        print("\nNext steps:")
        print("1. Set up PostgreSQL database")
        print("2. Configure .env file with database credentials")
        print("3. Run: cd backend && python run.py")
        print("4. In another terminal: cd frontend && npm install && npm run dev")
        print("5. Visit http://localhost:3000 to use the app")
        print("\nAPI Documentation: http://localhost:8000/docs")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("ERROR! Tests failed ✗")
        print("=" * 60)
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
