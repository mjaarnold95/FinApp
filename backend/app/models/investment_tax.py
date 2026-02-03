from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel


class TaxClassification(str, Enum):
    """Tax treatment classifications for investments"""
    PRE_TAX = "pre_tax"          # Traditional 401k, Traditional IRA
    ROTH = "roth"                 # Roth 401k, Roth IRA
    AFTER_TAX = "after_tax"      # After-tax 401k contributions
    TAXABLE = "taxable"          # Regular brokerage accounts


class InvestmentTaxBucket(SQLModel, table=True):
    """Tax bucket for tracking different tax treatments within an account"""
    __tablename__ = "investment_tax_buckets"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    account_id: int = Field(foreign_key="accounts.id", index=True)
    tax_classification: TaxClassification
    balance: Decimal = Field(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    cost_basis: Decimal = Field(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    contributions_ytd: Decimal = Field(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    earnings: Decimal = Field(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class InvestmentTransaction(SQLModel, table=True):
    """Transactions specific to investments with tax classification"""
    __tablename__ = "investment_transactions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    account_id: int = Field(foreign_key="accounts.id", index=True)
    tax_bucket_id: Optional[int] = Field(default=None, foreign_key="investment_tax_buckets.id")
    transaction_date: datetime = Field(index=True)
    transaction_type: str  # contribution, withdrawal, dividend, capital_gain, etc.
    tax_classification: TaxClassification
    amount: Decimal = Field(max_digits=15, decimal_places=2)
    description: str
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
