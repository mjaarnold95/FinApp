from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from ..core.database import get_session
from ..models.retirement import RetirementAccount

router = APIRouter(prefix="/retirement", tags=["retirement"])


@router.get("/", response_model=List[RetirementAccount])
def get_retirement_accounts(user_id: int = None, session: Session = Depends(get_session)):
    """Get all retirement accounts, optionally filtered by user"""
    query = select(RetirementAccount)
    if user_id:
        query = query.where(RetirementAccount.user_id == user_id)
    accounts = session.exec(query).all()
    return accounts


@router.get("/{retirement_id}", response_model=RetirementAccount)
def get_retirement_account(retirement_id: int, session: Session = Depends(get_session)):
    """Get a specific retirement account"""
    account = session.get(RetirementAccount, retirement_id)
    if not account:
        raise HTTPException(status_code=404, detail="Retirement account not found")
    return account


@router.post("/", response_model=RetirementAccount)
def create_retirement_account(account: RetirementAccount, session: Session = Depends(get_session)):
    """Create a new retirement account"""
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


@router.put("/{retirement_id}", response_model=RetirementAccount)
def update_retirement_account(retirement_id: int, account_data: RetirementAccount, session: Session = Depends(get_session)):
    """Update a retirement account"""
    account = session.get(RetirementAccount, retirement_id)
    if not account:
        raise HTTPException(status_code=404, detail="Retirement account not found")
    
    account_dict = account_data.model_dump(exclude_unset=True)
    for key, value in account_dict.items():
        setattr(account, key, value)
    
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


@router.delete("/{retirement_id}")
def delete_retirement_account(retirement_id: int, session: Session = Depends(get_session)):
    """Delete a retirement account"""
    account = session.get(RetirementAccount, retirement_id)
    if not account:
        raise HTTPException(status_code=404, detail="Retirement account not found")
    
    session.delete(account)
    session.commit()
    return {"message": "Retirement account deleted successfully"}
