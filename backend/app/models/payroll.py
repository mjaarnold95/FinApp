from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel


class Payroll(SQLModel, table=True):
    """Payroll model for tracking jobs and income"""
    __tablename__ = "payroll"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    employer_name: str
    job_title: str
    pay_period_start: datetime
    pay_period_end: datetime
    pay_date: datetime
    gross_pay: Decimal = Field(max_digits=15, decimal_places=2)
    net_pay: Decimal = Field(max_digits=15, decimal_places=2)
    year_to_date_gross: Decimal = Field(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    year_to_date_net: Decimal = Field(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Deduction(SQLModel, table=True):
    """Deduction model for payroll deductions"""
    __tablename__ = "deductions"

    id: Optional[int] = Field(default=None, primary_key=True)
    payroll_id: int = Field(foreign_key="payroll.id", index=True)
    deduction_type: str  # health_insurance, dental, vision, retirement_401k, hsa, fsa, etc.
    description: str
    amount: Decimal = Field(max_digits=15, decimal_places=2)
    is_pre_tax: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Withholding(SQLModel, table=True):
    """Withholding model for tax withholdings"""
    __tablename__ = "withholdings"

    id: Optional[int] = Field(default=None, primary_key=True)
    payroll_id: int = Field(foreign_key="payroll.id", index=True)
    withholding_type: str  # federal_income, state_income, social_security, medicare, local, etc.
    description: str
    amount: Decimal = Field(max_digits=15, decimal_places=2)
    year_to_date: Decimal = Field(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
