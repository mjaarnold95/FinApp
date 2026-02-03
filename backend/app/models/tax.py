from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel


class TaxRecord(SQLModel, table=True):
    """Tax record model for tracking tax information"""
    __tablename__ = "tax_records"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    tax_year: int = Field(index=True)
    filing_status: str  # single, married_filing_jointly, married_filing_separately, head_of_household
    gross_income: Decimal = Field(max_digits=15, decimal_places=2)
    adjusted_gross_income: Decimal = Field(max_digits=15, decimal_places=2)
    taxable_income: Decimal = Field(max_digits=15, decimal_places=2)
    total_tax: Decimal = Field(max_digits=15, decimal_places=2)
    federal_withholding: Decimal = Field(max_digits=15, decimal_places=2)
    state_withholding: Decimal = Field(max_digits=15, decimal_places=2)
    refund_or_owed: Decimal = Field(max_digits=15, decimal_places=2)
    filing_date: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
