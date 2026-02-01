from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from sqlmodel import Field, SQLModel


class Transaction(SQLModel, table=True):
    """Transaction model for financial transactions"""
    __tablename__ = "transactions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    account_id: int = Field(foreign_key="accounts.id", index=True)
    transaction_date: datetime = Field(index=True)
    description: str
    amount: Decimal = Field(max_digits=15, decimal_places=2)
    category: Optional[str] = None
    merchant: Optional[str] = None
    notes: Optional[str] = None
    is_recurring: bool = Field(default=False)
    plaid_transaction_id: Optional[str] = Field(default=None, unique=True, index=True)  # Plaid transaction ID for deduplication
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
