from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class PlaidItem(SQLModel, table=True):
    """Plaid item model for linked bank accounts"""
    __tablename__ = "plaid_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    account_id: Optional[int] = Field(default=None, foreign_key="accounts.id")
    plaid_item_id: str = Field(unique=True, index=True)
    plaid_access_token: str  # Encrypted in production
    institution_id: str
    institution_name: str
    last_synced: Optional[datetime] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PlaidAccount(SQLModel, table=True):
    """Plaid account model for individual accounts from bank"""
    __tablename__ = "plaid_accounts"

    id: Optional[int] = Field(default=None, primary_key=True)
    plaid_item_id: int = Field(foreign_key="plaid_items.id", index=True)
    account_id: int = Field(foreign_key="accounts.id", index=True)
    plaid_account_id: str = Field(unique=True, index=True)
    account_name: str
    account_mask: Optional[str] = None  # Last 4 digits
    account_type: str  # checking, savings, credit, etc.
    account_subtype: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
