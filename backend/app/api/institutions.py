from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from ..core.database import get_session
from ..models.financial_institution import FinancialInstitution

router = APIRouter(prefix="/institutions", tags=["institutions"])


@router.get("/", response_model=List[FinancialInstitution])
def get_institutions(session: Session = Depends(get_session)):
    """Get all financial institutions"""
    institutions = session.exec(select(FinancialInstitution)).all()
    return institutions


@router.get("/{institution_id}", response_model=FinancialInstitution)
def get_institution(institution_id: int, session: Session = Depends(get_session)):
    """Get a specific financial institution"""
    institution = session.get(FinancialInstitution, institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    return institution


@router.post("/", response_model=FinancialInstitution)
def create_institution(institution: FinancialInstitution, session: Session = Depends(get_session)):
    """Create a new financial institution"""
    session.add(institution)
    session.commit()
    session.refresh(institution)
    return institution


@router.put("/{institution_id}", response_model=FinancialInstitution)
def update_institution(institution_id: int, institution_data: FinancialInstitution, session: Session = Depends(get_session)):
    """Update a financial institution"""
    institution = session.get(FinancialInstitution, institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    
    institution_dict = institution_data.model_dump(exclude_unset=True)
    for key, value in institution_dict.items():
        setattr(institution, key, value)
    
    session.add(institution)
    session.commit()
    session.refresh(institution)
    return institution


@router.delete("/{institution_id}")
def delete_institution(institution_id: int, session: Session = Depends(get_session)):
    """Delete a financial institution"""
    institution = session.get(FinancialInstitution, institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    
    session.delete(institution)
    session.commit()
    return {"message": "Institution deleted successfully"}
