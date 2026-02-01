from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from decimal import Decimal

from ..core.database import get_session
from ..models.investment_tax import InvestmentTaxBucket, InvestmentTransaction, TaxClassification
from ..models.account import Account
from pydantic import BaseModel

router = APIRouter(prefix="/investment-tax", tags=["investment-tax"])


class TaxBucketCreate(BaseModel):
    account_id: int
    tax_classification: TaxClassification
    initial_balance: Decimal = Decimal("0.00")


class InvestmentTransactionCreate(BaseModel):
    user_id: int
    account_id: int
    tax_bucket_id: int
    transaction_type: str
    tax_classification: TaxClassification
    amount: Decimal
    description: str
    notes: str = None


@router.get("/buckets/account/{account_id}", response_model=List[InvestmentTaxBucket])
def get_account_tax_buckets(account_id: int, session: Session = Depends(get_session)):
    """Get all tax buckets for an account"""
    buckets = session.exec(
        select(InvestmentTaxBucket).where(InvestmentTaxBucket.account_id == account_id)
    ).all()
    return buckets


@router.post("/buckets", response_model=InvestmentTaxBucket)
def create_tax_bucket(bucket: TaxBucketCreate, session: Session = Depends(get_session)):
    """Create a new tax bucket for an account"""
    # Check if account exists
    account = session.get(Account, bucket.account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Check if bucket already exists for this tax classification
    existing = session.exec(
        select(InvestmentTaxBucket).where(
            InvestmentTaxBucket.account_id == bucket.account_id,
            InvestmentTaxBucket.tax_classification == bucket.tax_classification
        )
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Tax bucket for {bucket.tax_classification} already exists in this account"
        )
    
    # Create bucket
    db_bucket = InvestmentTaxBucket(
        account_id=bucket.account_id,
        tax_classification=bucket.tax_classification,
        balance=bucket.initial_balance,
        cost_basis=bucket.initial_balance
    )
    session.add(db_bucket)
    session.commit()
    session.refresh(db_bucket)
    return db_bucket


@router.get("/buckets/{bucket_id}", response_model=InvestmentTaxBucket)
def get_tax_bucket(bucket_id: int, session: Session = Depends(get_session)):
    """Get a specific tax bucket"""
    bucket = session.get(InvestmentTaxBucket, bucket_id)
    if not bucket:
        raise HTTPException(status_code=404, detail="Tax bucket not found")
    return bucket


@router.post("/transactions", response_model=InvestmentTransaction)
def create_investment_transaction(
    transaction: InvestmentTransactionCreate,
    session: Session = Depends(get_session)
):
    """Create an investment transaction and update tax bucket"""
    # Verify tax bucket exists
    tax_bucket = session.get(InvestmentTaxBucket, transaction.tax_bucket_id)
    if not tax_bucket:
        raise HTTPException(status_code=404, detail="Tax bucket not found")
    
    # Create transaction
    from datetime import datetime, timezone
    db_transaction = InvestmentTransaction(
        user_id=transaction.user_id,
        account_id=transaction.account_id,
        tax_bucket_id=transaction.tax_bucket_id,
        transaction_date=datetime.now(timezone.utc),
        transaction_type=transaction.transaction_type,
        tax_classification=transaction.tax_classification,
        amount=transaction.amount,
        description=transaction.description,
        notes=transaction.notes
    )
    session.add(db_transaction)
    
    # Update tax bucket balance based on transaction type
    if transaction.transaction_type in ["contribution", "deposit", "dividend", "interest"]:
        tax_bucket.balance += transaction.amount
        if transaction.transaction_type == "contribution":
            tax_bucket.cost_basis += transaction.amount
            tax_bucket.contributions_ytd += transaction.amount
    elif transaction.transaction_type in ["withdrawal", "distribution"]:
        tax_bucket.balance -= transaction.amount
    elif transaction.transaction_type == "capital_gain":
        tax_bucket.earnings += transaction.amount
        tax_bucket.balance += transaction.amount
    
    session.add(tax_bucket)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction


@router.get("/transactions/account/{account_id}", response_model=List[InvestmentTransaction])
def get_account_investment_transactions(
    account_id: int,
    session: Session = Depends(get_session)
):
    """Get all investment transactions for an account"""
    transactions = session.exec(
        select(InvestmentTransaction).where(InvestmentTransaction.account_id == account_id)
    ).all()
    return transactions


@router.get("/account/{account_id}/summary")
def get_account_tax_summary(account_id: int, session: Session = Depends(get_session)):
    """Get summary of tax buckets for an account"""
    buckets = session.exec(
        select(InvestmentTaxBucket).where(InvestmentTaxBucket.account_id == account_id)
    ).all()
    
    total_balance = sum(bucket.balance for bucket in buckets)
    
    summary = {
        "account_id": account_id,
        "total_balance": float(total_balance),
        "buckets": [
            {
                "tax_classification": bucket.tax_classification,
                "balance": float(bucket.balance),
                "cost_basis": float(bucket.cost_basis),
                "earnings": float(bucket.earnings),
                "contributions_ytd": float(bucket.contributions_ytd),
                "percentage": float((bucket.balance / total_balance * 100) if total_balance > 0 else 0)
            }
            for bucket in buckets
        ]
    }
    
    return summary
