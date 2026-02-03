from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel


class RetirementForecast(SQLModel, table=True):
    """Retirement forecast with Monte Carlo simulation results"""
    __tablename__ = "retirement_forecasts"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    forecast_name: str

    # Input parameters
    current_age: int
    retirement_age: int
    life_expectancy: int = 95
    current_savings: Decimal = Field(max_digits=15, decimal_places=2)
    annual_contribution: Decimal = Field(max_digits=15, decimal_places=2)
    expected_return: Decimal = Field(max_digits=5, decimal_places=2)  # Annual percentage
    volatility: Decimal = Field(max_digits=5, decimal_places=2)  # Standard deviation
    inflation_rate: Decimal = Field(max_digits=5, decimal_places=2, default=Decimal("2.5"))

    # Withdrawal strategy
    annual_withdrawal: Decimal = Field(max_digits=15, decimal_places=2)
    withdrawal_strategy: str = "fixed"  # fixed, percentage, rmd

    # Monte Carlo parameters
    num_simulations: int = 10000
    success_threshold: Decimal = Field(max_digits=5, decimal_places=2, default=Decimal("80.00"))

    # Results
    success_rate: Optional[Decimal] = Field(default=None, max_digits=5, decimal_places=2)
    median_final_balance: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    percentile_10_balance: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    percentile_90_balance: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)

    # RMD projections
    first_rmd_year: Optional[int] = None
    first_rmd_amount: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)

    # IRMAA considerations
    estimated_magi: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    irmaa_bracket: Optional[str] = None  # standard, tier1, tier2, tier3, tier4

    # Metadata
    simulation_data: Optional[str] = None  # JSON blob for detailed results
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_run: Optional[datetime] = None


class RMDProjection(SQLModel, table=True):
    """Required Minimum Distribution projections"""
    __tablename__ = "rmd_projections"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    forecast_id: Optional[int] = Field(default=None, foreign_key="retirement_forecasts.id")

    year: int
    age: int
    account_balance: Decimal = Field(max_digits=15, decimal_places=2)
    rmd_amount: Decimal = Field(max_digits=15, decimal_places=2)
    life_expectancy_factor: Decimal = Field(max_digits=5, decimal_places=2)

    # Tax bucket breakdown
    pre_tax_balance: Decimal = Field(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    roth_balance: Decimal = Field(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    after_tax_balance: Decimal = Field(max_digits=15, decimal_places=2, default=Decimal("0.00"))

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class IRMAAProjection(SQLModel, table=True):
    """IRMAA (Income-Related Monthly Adjustment Amount) projections"""
    __tablename__ = "irmaa_projections"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    forecast_id: Optional[int] = Field(default=None, foreign_key="retirement_forecasts.id")

    year: int
    age: int

    # Income components
    social_security: Decimal = Field(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    pension: Decimal = Field(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    investment_income: Decimal = Field(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    rmd_income: Decimal = Field(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    other_income: Decimal = Field(max_digits=15, decimal_places=2, default=Decimal("0.00"))

    # MAGI calculation
    adjusted_gross_income: Decimal = Field(max_digits=15, decimal_places=2)
    magi: Decimal = Field(max_digits=15, decimal_places=2)

    # IRMAA tier (2024 brackets, will need annual updates)
    irmaa_tier: str  # standard, tier1, tier2, tier3, tier4, tier5
    monthly_premium_surcharge: Decimal = Field(max_digits=10, decimal_places=2)
    annual_premium_surcharge: Decimal = Field(max_digits=10, decimal_places=2)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RetirementScenario(SQLModel, table=True):
    """Different retirement scenarios for comparison"""
    __tablename__ = "retirement_scenarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    scenario_name: str
    description: Optional[str] = None

    # Scenario parameters
    retirement_age: int
    annual_contribution: Decimal = Field(max_digits=15, decimal_places=2)
    withdrawal_rate: Decimal = Field(max_digits=5, decimal_places=2)

    # Roth conversion strategy
    roth_conversion_amount: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    roth_conversion_years: Optional[int] = None

    # Results comparison
    success_rate: Optional[Decimal] = Field(default=None, max_digits=5, decimal_places=2)
    total_taxes_paid: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)
    estate_value: Optional[Decimal] = Field(default=None, max_digits=15, decimal_places=2)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
