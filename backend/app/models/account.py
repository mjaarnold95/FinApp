from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel


class AccountType(str, Enum):
    """Types of accounts"""
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT_CARD = "credit_card"
    INVESTMENT = "investment"
    LOAN = "loan"
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"


class Account(SQLModel, table=True):
    """Account model for all types of accounts"""
    __tablename__ = "accounts"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    institution_id: Optional[int] = Field(default=None, foreign_key="financial_institutions.id")
    name: str
    account_type: AccountType
    account_number: Optional[str] = None
    balance: Decimal = Field(default=Decimal("0.00"), max_digits=15, decimal_places=2)
    currency: str = Field(default="USD")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
