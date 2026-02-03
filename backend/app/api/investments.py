from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from ..core.database import get_session
from ..models.investment import Investment

router = APIRouter(prefix="/investments", tags=["investments"])


@router.get("/", response_model=List[Investment])
def get_investments(user_id: int = None, session: Session = Depends(get_session)):
    """Get all investments, optionally filtered by user"""
    query = select(Investment)
    if user_id:
        query = query.where(Investment.user_id == user_id)
    investments = session.exec(query).all()
    return investments


@router.get("/{investment_id}", response_model=Investment)
def get_investment(investment_id: int, session: Session = Depends(get_session)):
    """Get a specific investment"""
    investment = session.get(Investment, investment_id)
    if not investment:
        raise HTTPException(status_code=404, detail="Investment not found")
    return investment


@router.post("/", response_model=Investment)
def create_investment(investment: Investment, session: Session = Depends(get_session)):
    """Create a new investment"""
    session.add(investment)
    session.commit()
    session.refresh(investment)
    return investment


@router.put("/{investment_id}", response_model=Investment)
def update_investment(investment_id: int, investment_data: Investment, session: Session = Depends(get_session)):
    """Update an investment"""
    investment = session.get(Investment, investment_id)
    if not investment:
        raise HTTPException(status_code=404, detail="Investment not found")
    
    investment_dict = investment_data.model_dump(exclude_unset=True)
    for key, value in investment_dict.items():
        setattr(investment, key, value)
    
    session.add(investment)
    session.commit()
    session.refresh(investment)
    return investment


@router.delete("/{investment_id}")
def delete_investment(investment_id: int, session: Session = Depends(get_session)):
    """Delete an investment"""
    investment = session.get(Investment, investment_id)
    if not investment:
        raise HTTPException(status_code=404, detail="Investment not found")
    
    session.delete(investment)
    session.commit()
    return {"message": "Investment deleted successfully"}
