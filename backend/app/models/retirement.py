from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel


class RetirementType(str, Enum):
    """Types of retirement accounts"""
    IRA_TRADITIONAL = "ira_traditional"
    IRA_ROTH = "ira_roth"
    K401_TRADITIONAL = "401k_traditional"
    K401_ROTH = "401k_roth"
    K403B = "403b"
    K457 = "457"
    SEP_IRA = "sep_ira"
    SIMPLE_IRA = "simple_ira"
    PENSION = "pension"
    OTHER = "other"


class RetirementAccount(SQLModel, table=True):
    """Retirement account model"""
    __tablename__ = "retirement_accounts"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    account_id: int = Field(foreign_key="accounts.id", index=True)
    retirement_type: RetirementType
    account_name: str
    balance: Decimal = Field(max_digits=15, decimal_places=2)
    contribution_limit: Decimal = Field(max_digits=15, decimal_places=2)
    year_to_date_contribution: Decimal = Field(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    employer_match_percent: Optional[Decimal] = Field(default=None, max_digits=5, decimal_places=2)
    vesting_percentage: Decimal = Field(max_digits=5, decimal_places=2, default=Decimal("100.00"))
    beneficiary: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
