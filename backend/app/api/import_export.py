from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select
from typing import List
import csv
import io
from datetime import datetime
from decimal import Decimal

from ..core.database import get_session
from ..models.user import User
from ..models.account import Account
from ..models.transaction import Transaction
from ..models.investment import Investment
from ..models.payroll import Payroll
from pydantic import BaseModel

router = APIRouter(prefix="/import-export", tags=["import-export"])


class ImportStats(BaseModel):
    total_rows: int
    imported: int
    skipped: int
    errors: List[str]


@router.post("/transactions/import")
async def import_transactions(
    user_id: int,
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
) -> ImportStats:
    """
    Import transactions from CSV file
    Expected columns: date, description, amount, category, account_id
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    csv_content = content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(csv_content))
    
    stats = ImportStats(total_rows=0, imported=0, skipped=0, errors=[])
    
    for row in csv_reader:
        stats.total_rows += 1
        try:
            # Parse transaction data
            transaction = Transaction(
                user_id=user_id,
                account_id=int(row.get('account_id', 0)),
                transaction_date=datetime.strptime(row.get('date', ''), '%Y-%m-%d'),
                description=row.get('description', ''),
                amount=Decimal(row.get('amount', '0.00')),
                category=row.get('category', ''),
                merchant=row.get('merchant', '')
            )
            
            session.add(transaction)
            session.commit()
            stats.imported += 1
        except Exception as e:
            stats.skipped += 1
            stats.errors.append(f"Row {stats.total_rows}: {str(e)}")
            session.rollback()
    
    return stats


@router.get("/transactions/export")
def export_transactions(
    user_id: int,
    session: Session = Depends(get_session)
):
    """Export user transactions to CSV"""
    transactions = session.exec(
        select(Transaction).where(Transaction.user_id == user_id)
    ).all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['date', 'description', 'amount', 'category', 'merchant', 'account_id'])
    
    # Write data
    for txn in transactions:
        writer.writerow([
            txn.transaction_date.strftime('%Y-%m-%d'),
            txn.description,
            str(txn.amount),
            txn.category or '',
            txn.merchant or '',
            txn.account_id
        ])
    
    output.seek(0)
    
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=transactions_{user_id}.csv"}
    )


@router.post("/accounts/import")
async def import_accounts(
    user_id: int,
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
) -> ImportStats:
    """
    Import accounts from CSV file
    Expected columns: name, account_type, balance, currency
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    csv_content = content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(csv_content))
    
    stats = ImportStats(total_rows=0, imported=0, skipped=0, errors=[])
    
    for row in csv_reader:
        stats.total_rows += 1
        try:
            account = Account(
                user_id=user_id,
                name=row.get('name', ''),
                account_type=row.get('account_type', 'checking'),
                balance=Decimal(row.get('balance', '0.00')),
                currency=row.get('currency', 'USD')
            )
            
            session.add(account)
            session.commit()
            stats.imported += 1
        except Exception as e:
            stats.skipped += 1
            stats.errors.append(f"Row {stats.total_rows}: {str(e)}")
            session.rollback()
    
    return stats


@router.get("/accounts/export")
def export_accounts(
    user_id: int,
    session: Session = Depends(get_session)
):
    """Export user accounts to CSV"""
    accounts = session.exec(
        select(Account).where(Account.user_id == user_id)
    ).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['name', 'account_type', 'balance', 'currency', 'is_active'])
    
    for acc in accounts:
        writer.writerow([
            acc.name,
            acc.account_type.value,
            str(acc.balance),
            acc.currency,
            acc.is_active
        ])
    
    output.seek(0)
    
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=accounts_{user_id}.csv"}
    )


@router.post("/investments/import")
async def import_investments(
    user_id: int,
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
) -> ImportStats:
    """
    Import investments from CSV file
    Expected columns: symbol, name, investment_type, quantity, purchase_price, current_price, purchase_date, account_id
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    csv_content = content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(csv_content))
    
    stats = ImportStats(total_rows=0, imported=0, skipped=0, errors=[])
    
    for row in csv_reader:
        stats.total_rows += 1
        try:
            investment = Investment(
                user_id=user_id,
                account_id=int(row.get('account_id', 0)),
                investment_type=row.get('investment_type', 'stock'),
                symbol=row.get('symbol', ''),
                name=row.get('name', ''),
                quantity=Decimal(row.get('quantity', '0')),
                purchase_price=Decimal(row.get('purchase_price', '0.00')),
                current_price=Decimal(row.get('current_price', '0.00')),
                purchase_date=datetime.strptime(row.get('purchase_date', ''), '%Y-%m-%d')
            )
            
            session.add(investment)
            session.commit()
            stats.imported += 1
        except Exception as e:
            stats.skipped += 1
            stats.errors.append(f"Row {stats.total_rows}: {str(e)}")
            session.rollback()
    
    return stats


@router.get("/investments/export")
def export_investments(
    user_id: int,
    session: Session = Depends(get_session)
):
    """Export user investments to CSV"""
    investments = session.exec(
        select(Investment).where(Investment.user_id == user_id)
    ).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        'symbol', 'name', 'investment_type', 'quantity', 
        'purchase_price', 'current_price', 'purchase_date', 'account_id'
    ])
    
    for inv in investments:
        writer.writerow([
            inv.symbol,
            inv.name,
            inv.investment_type.value,
            str(inv.quantity),
            str(inv.purchase_price),
            str(inv.current_price),
            inv.purchase_date.strftime('%Y-%m-%d'),
            inv.account_id
        ])
    
    output.seek(0)
    
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=investments_{user_id}.csv"}
    )
