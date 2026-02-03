from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..core.database import get_session
from ..models.account import Account
from ..models.ledger import LedgerEntry, EntryType
from ..models.transaction import Transaction

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/", response_model=List[Transaction])
def get_transactions(user_id: int = None, account_id: int = None, session: Session = Depends(get_session)):
    """Get all transactions, optionally filtered by user or account"""
    query = select(Transaction)
    if user_id:
        query = query.where(Transaction.user_id == user_id)
    if account_id:
        query = query.where(Transaction.account_id == account_id)
    transactions = session.exec(query).all()
    return transactions


@router.get("/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: int, session: Session = Depends(get_session)):
    """Get a specific transaction"""
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.post("/", response_model=Transaction)
def create_transaction(transaction: Transaction, session: Session = Depends(get_session)):
    """Create a new transaction with double-entry ledger entries"""
    # Add transaction
    session.add(transaction)
    session.commit()
    session.refresh(transaction)

    # Create ledger entries (double-entry accounting)
    # Debit entry for the account
    debit_entry = LedgerEntry(
        user_id=transaction.user_id,
        transaction_id=transaction.id,
        account_id=transaction.account_id,
        entry_type=EntryType.DEBIT if transaction.amount > 0 else EntryType.CREDIT,
        amount=abs(transaction.amount),
        entry_date=transaction.transaction_date,
        description=transaction.description,
    )
    session.add(debit_entry)

    # Update account balance
    account = session.get(Account, transaction.account_id)
    if account:
        account.balance += transaction.amount
        account.updated_at = datetime.now(timezone.utc)
        session.add(account)

    session.commit()
    return transaction


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, session: Session = Depends(get_session)):
    """Delete a transaction"""
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    session.delete(transaction)
    session.commit()
    return {"message": "Transaction deleted successfully"}
