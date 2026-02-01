from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from ..core.database import get_session
from ..models.payroll import Payroll, Deduction, Withholding

router = APIRouter(prefix="/payroll", tags=["payroll"])


@router.get("/", response_model=List[Payroll])
def get_payroll_records(user_id: int = None, session: Session = Depends(get_session)):
    """Get all payroll records, optionally filtered by user"""
    query = select(Payroll)
    if user_id:
        query = query.where(Payroll.user_id == user_id)
    records = session.exec(query).all()
    return records


@router.get("/{payroll_id}", response_model=Payroll)
def get_payroll_record(payroll_id: int, session: Session = Depends(get_session)):
    """Get a specific payroll record"""
    record = session.get(Payroll, payroll_id)
    if not record:
        raise HTTPException(status_code=404, detail="Payroll record not found")
    return record


@router.post("/", response_model=Payroll)
def create_payroll_record(payroll: Payroll, session: Session = Depends(get_session)):
    """Create a new payroll record"""
    session.add(payroll)
    session.commit()
    session.refresh(payroll)
    return payroll


@router.get("/{payroll_id}/deductions", response_model=List[Deduction])
def get_deductions(payroll_id: int, session: Session = Depends(get_session)):
    """Get deductions for a payroll record"""
    deductions = session.exec(select(Deduction).where(Deduction.payroll_id == payroll_id)).all()
    return deductions


@router.post("/{payroll_id}/deductions", response_model=Deduction)
def create_deduction(payroll_id: int, deduction: Deduction, session: Session = Depends(get_session)):
    """Create a new deduction"""
    deduction.payroll_id = payroll_id
    session.add(deduction)
    session.commit()
    session.refresh(deduction)
    return deduction


@router.get("/{payroll_id}/withholdings", response_model=List[Withholding])
def get_withholdings(payroll_id: int, session: Session = Depends(get_session)):
    """Get withholdings for a payroll record"""
    withholdings = session.exec(select(Withholding).where(Withholding.payroll_id == payroll_id)).all()
    return withholdings


@router.post("/{payroll_id}/withholdings", response_model=Withholding)
def create_withholding(payroll_id: int, withholding: Withholding, session: Session = Depends(get_session)):
    """Create a new withholding"""
    withholding.payroll_id = payroll_id
    session.add(withholding)
    session.commit()
    session.refresh(withholding)
    return withholding
