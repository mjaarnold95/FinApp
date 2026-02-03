from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from ..core.database import get_session
from ..models.tax import TaxRecord

router = APIRouter(prefix="/taxes", tags=["taxes"])


@router.get("/", response_model=List[TaxRecord])
def get_tax_records(user_id: int = None, tax_year: int = None, session: Session = Depends(get_session)):
    """Get all tax records, optionally filtered by user and year"""
    query = select(TaxRecord)
    if user_id:
        query = query.where(TaxRecord.user_id == user_id)
    if tax_year:
        query = query.where(TaxRecord.tax_year == tax_year)
    records = session.exec(query).all()
    return records


@router.get("/{tax_id}", response_model=TaxRecord)
def get_tax_record(tax_id: int, session: Session = Depends(get_session)):
    """Get a specific tax record"""
    record = session.get(TaxRecord, tax_id)
    if not record:
        raise HTTPException(status_code=404, detail="Tax record not found")
    return record


@router.post("/", response_model=TaxRecord)
def create_tax_record(tax_record: TaxRecord, session: Session = Depends(get_session)):
    """Create a new tax record"""
    session.add(tax_record)
    session.commit()
    session.refresh(tax_record)
    return tax_record


@router.put("/{tax_id}", response_model=TaxRecord)
def update_tax_record(tax_id: int, tax_data: TaxRecord, session: Session = Depends(get_session)):
    """Update a tax record"""
    record = session.get(TaxRecord, tax_id)
    if not record:
        raise HTTPException(status_code=404, detail="Tax record not found")
    
    tax_dict = tax_data.model_dump(exclude_unset=True)
    for key, value in tax_dict.items():
        setattr(record, key, value)
    
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


@router.delete("/{tax_id}")
def delete_tax_record(tax_id: int, session: Session = Depends(get_session)):
    """Delete a tax record"""
    record = session.get(TaxRecord, tax_id)
    if not record:
        raise HTTPException(status_code=404, detail="Tax record not found")
    
    session.delete(record)
    session.commit()
    return {"message": "Tax record deleted successfully"}
