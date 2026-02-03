from datetime import datetime, timezone
from decimal import Decimal
from enum import StrEnum, auto
from typing import Optional

from sqlmodel import Field, SQLModel


class EntryType(StrEnum):
    """Double-entry accounting entry types"""
    DEBIT = auto()
    CREDIT = auto()


class LedgerEntry(SQLModel, table=True):
    """Ledger entry model for double-entry accounting"""
    __tablename__ = "ledger_entries"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    transaction_id: int = Field(foreign_key="transactions.id", index=True)
    account_id: int = Field(foreign_key="accounts.id", index=True)
    entry_type: EntryType
    amount: Decimal = Field(max_digits=15, decimal_places=2)
    entry_date: datetime = Field(index=True)
    description: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        """SQLModel configuration"""
        arbitrary_types_allowed = True
