from datetime import datetime, timezone
from decimal import Decimal
from enum import StrEnum, auto
from typing import Optional

from sqlmodel import Field, SQLModel


class RetirementType(StrEnum):
    """Types of retirement accounts"""
    IRA_TRADITIONAL = auto()
    IRA_ROTH = auto()
    K401_TRADITIONAL = auto()
    K401_ROTH = auto()
    K403B = auto()
    K457 = auto()
    SEP_IRA = auto()
    SIMPLE_IRA = auto()
    PENSION = auto()
    OTHER = auto()


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
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
