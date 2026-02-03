from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel


class InvestmentType(str, Enum):
    """Types of investments"""
    STOCK = "stock"
    BOND = "bond"
    MUTUAL_FUND = "mutual_fund"
    ETF = "etf"
    CRYPTO = "crypto"
    REAL_ESTATE = "real_estate"
    COMMODITY = "commodity"
    OTHER = "other"


class Investment(SQLModel, table=True):
    """Investment model for tracking investments"""
    __tablename__ = "investments"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    account_id: int = Field(foreign_key="accounts.id", index=True)
    investment_type: InvestmentType
    symbol: str = Field(index=True)
    name: str
    quantity: Decimal = Field(max_digits=15, decimal_places=6)
    purchase_price: Decimal = Field(max_digits=15, decimal_places=2)
    current_price: Decimal = Field(max_digits=15, decimal_places=2)
    purchase_date: datetime
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
