from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class FinancialInstitution(SQLModel, table=True):
    """Financial institution model for banks, credit unions, etc."""
    __tablename__ = "financial_institutions"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    institution_type: str  # bank, credit_union, brokerage, etc.
    routing_number: Optional[str] = None
    swift_code: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
