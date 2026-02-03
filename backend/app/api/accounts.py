from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from ..core.database import get_session
from ..models.account import Account

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/", response_model=List[Account])
def get_accounts(user_id: int = None, session: Session = Depends(get_session)):
    """Get all accounts, optionally filtered by user"""
    query = select(Account)
    if user_id:
        query = query.where(Account.user_id == user_id)
    accounts = session.exec(query).all()
    return accounts


@router.get("/{account_id}", response_model=Account)
def get_account(account_id: int, session: Session = Depends(get_session)):
    """Get a specific account"""
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.post("/", response_model=Account)
def create_account(account: Account, session: Session = Depends(get_session)):
    """Create a new account"""
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


@router.put("/{account_id}", response_model=Account)
def update_account(account_id: int, account_data: Account, session: Session = Depends(get_session)):
    """Update an account"""
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account_dict = account_data.model_dump(exclude_unset=True)
    for key, value in account_dict.items():
        setattr(account, key, value)
    
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


@router.delete("/{account_id}")
def delete_account(account_id: int, session: Session = Depends(get_session)):
    """Delete an account"""
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    session.delete(account)
    session.commit()
    return {"message": "Account deleted successfully"}
