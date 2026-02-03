import json
from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from ..core.database import get_session
from ..models.investment_tax import InvestmentTaxBucket
from ..models.retirement_forecast import (
    RetirementForecast,
    RMDProjection,
    IRMAAProjection,
)
from ..services.monte_carlo_service import MonteCarloSimulator, RMDCalculator, IRMAACalculator

router = APIRouter(prefix="/retirement-forecast", tags=["retirement-forecast"])


class ForecastRequest(BaseModel):
    forecast_name: str
    current_age: int
    retirement_age: int
    life_expectancy: int = 95
    current_savings: Decimal
    annual_contribution: Decimal
    annual_withdrawal: Decimal
    expected_return: Decimal
    volatility: Decimal
    inflation_rate: Decimal = Decimal("2.5")
    num_simulations: int = 10000


@router.post("/forecast", response_model=RetirementForecast)
def create_retirement_forecast(
    user_id: int,
    forecast: ForecastRequest,
    session: Session = Depends(get_session),
):
    """Create and run a new retirement forecast with Monte Carlo simulation"""

    # Create forecast record
    db_forecast = RetirementForecast(
        user_id=user_id,
        forecast_name=forecast.forecast_name,
        current_age=forecast.current_age,
        retirement_age=forecast.retirement_age,
        life_expectancy=forecast.life_expectancy,
        current_savings=forecast.current_savings,
        annual_contribution=forecast.annual_contribution,
        annual_withdrawal=forecast.annual_withdrawal,
        expected_return=forecast.expected_return,
        volatility=forecast.volatility,
        inflation_rate=forecast.inflation_rate,
        num_simulations=forecast.num_simulations,
    )

    # Run Monte Carlo simulation
    simulator = MonteCarloSimulator(
        current_age=forecast.current_age,
        retirement_age=forecast.retirement_age,
        life_expectancy=forecast.life_expectancy,
        current_savings=forecast.current_savings,
        annual_contribution=forecast.annual_contribution,
        annual_withdrawal=forecast.annual_withdrawal,
        expected_return=forecast.expected_return,
        volatility=forecast.volatility,
        inflation_rate=forecast.inflation_rate,
        num_simulations=forecast.num_simulations,
    )

    results = simulator.run_simulation()

    # Update forecast with results
    db_forecast.success_rate = results["success_rate"]
    db_forecast.median_final_balance = results["median_final_balance"]
    db_forecast.percentile_10_balance = results["percentile_10_balance"]
    db_forecast.percentile_90_balance = results["percentile_90_balance"]
    db_forecast.simulation_data = json.dumps(results["year_stats"])

    from datetime import datetime, timezone
    db_forecast.last_run = datetime.now(timezone.utc)

    session.add(db_forecast)
    session.commit()
    session.refresh(db_forecast)

    return db_forecast


@router.get("/forecast/{forecast_id}", response_model=RetirementForecast)
def get_forecast(forecast_id: int, session: Session = Depends(get_session)):
    """Get a specific retirement forecast"""
    forecast = session.get(RetirementForecast, forecast_id)
    if not forecast:
        raise HTTPException(status_code=404, detail="Forecast not found")
    return forecast


@router.get("/forecasts/user/{user_id}", response_model=List[RetirementForecast])
def get_user_forecasts(user_id: int, session: Session = Depends(get_session)):
    """Get all forecasts for a user"""
    forecasts = session.exec(
        select(RetirementForecast).where(RetirementForecast.user_id == user_id),
    ).all()
    return forecasts


@router.get("/forecast/{forecast_id}/details")
def get_forecast_details(forecast_id: int, session: Session = Depends(get_session)):
    """Get detailed forecast results including year-by-year projections"""
    forecast = session.get(RetirementForecast, forecast_id)
    if not forecast:
        raise HTTPException(status_code=404, detail="Forecast not found")

    year_stats = json.loads(forecast.simulation_data) if forecast.simulation_data else []

    return {
        "forecast_id": forecast.id,
        "forecast_name": forecast.forecast_name,
        "success_rate": float(forecast.success_rate) if forecast.success_rate else 0,
        "median_final_balance": float(forecast.median_final_balance) if forecast.median_final_balance else 0,
        "percentile_10_balance": float(forecast.percentile_10_balance) if forecast.percentile_10_balance else 0,
        "percentile_90_balance": float(forecast.percentile_90_balance) if forecast.percentile_90_balance else 0,
        "year_projections": year_stats,
    }


class RMDRequest(BaseModel):
    starting_age: int = 73
    ending_age: int = 100
    pre_tax_balance: Decimal
    expected_return: Decimal
    additional_withdrawals: Decimal = Decimal("0.00")


@router.post("/rmd/project")
def project_rmds(
    user_id: int,
    forecast_id: Optional[int] = None,
    request: RMDRequest = ...,
    session: Session = Depends(get_session),
):
    """
    Project Required Minimum Distributions
    
    Args:
        user_id: User ID (required)
        forecast_id: Optional forecast ID to link projections to
        request: RMD projection parameters
        session: Database session
    """

    # Calculate RMD projections
    projections = RMDCalculator.project_rmds(
        starting_age=request.starting_age,
        ending_age=request.ending_age,
        pre_tax_balance=request.pre_tax_balance,
        expected_return=request.expected_return,
        additional_withdrawals=request.additional_withdrawals,
    )

    # Save projections to database
    for proj in projections:
        db_proj = RMDProjection(
            user_id=user_id,
            forecast_id=forecast_id,
            year=proj["year"],
            age=proj["age"],
            account_balance=Decimal(str(proj["account_balance"])),
            rmd_amount=Decimal(str(proj["rmd_amount"])),
            life_expectancy_factor=Decimal(str(proj["life_expectancy_factor"])),
            pre_tax_balance=Decimal(str(proj["account_balance"])),
        )
        session.add(db_proj)

    session.commit()

    return {
        "user_id": user_id,
        "forecast_id": forecast_id,
        "projections": projections,
    }


@router.get("/rmd/user/{user_id}")
def get_user_rmd_projections(
    user_id: int,
    forecast_id: Optional[int] = None,
    session: Session = Depends(get_session),
):
    """Get RMD projections for a user"""
    query = select(RMDProjection).where(RMDProjection.user_id == user_id)

    if forecast_id:
        query = query.where(RMDProjection.forecast_id == forecast_id)

    projections = session.exec(query).all()

    return {
        "user_id": user_id,
        "forecast_id": forecast_id,
        "projections": [
            {
                "year": p.year,
                "age": p.age,
                "account_balance": float(p.account_balance),
                "rmd_amount": float(p.rmd_amount),
                "life_expectancy_factor": float(p.life_expectancy_factor),
            }
            for p in projections
        ],
    }


class IRMAARequest(BaseModel):
    starting_age: int = 65
    ending_age: int = 95
    social_security: Decimal = Decimal("0.00")
    pension: Decimal = Decimal("0.00")
    investment_income: Decimal = Decimal("0.00")
    other_income: Decimal = Decimal("0.00")
    filing_status: str = "single"


@router.post("/irmaa/project")
def project_irmaa(
    user_id: int,
    forecast_id: Optional[int] = None,
    request: IRMAARequest = ...,
    session: Session = Depends(get_session),
):
    """
    Project IRMAA (Medicare surcharges) based on income
    
    Args:
        user_id: User ID (required)
        forecast_id: Optional forecast ID to link projections to and use RMD data
        request: IRMAA projection parameters
        session: Database session
    """

    # Get RMD projections if they exist
    rmd_projections = []
    if forecast_id:
        rmd_data = session.exec(
            select(RMDProjection).where(
                RMDProjection.user_id == user_id,
                RMDProjection.forecast_id == forecast_id,
            ),
        ).all()
        rmd_projections = [
            {
                "age": r.age,
                "rmd_amount": float(r.rmd_amount),
            }
            for r in rmd_data
        ]

    # Calculate IRMAA projections
    income_sources = {
        "social_security": request.social_security,
        "pension": request.pension,
        "investment_income": request.investment_income,
        "other_income": request.other_income,
    }

    projections = IRMAACalculator.project_irmaa(
        starting_age=request.starting_age,
        ending_age=request.ending_age,
        income_sources=income_sources,
        rmd_projections=rmd_projections,
        filing_status=request.filing_status,
    )

    # Save to database
    for proj in projections:
        db_proj = IRMAAProjection(
            user_id=user_id,
            forecast_id=forecast_id,
            year=proj["year"],
            age=proj["age"],
            social_security=request.social_security,
            pension=request.pension,
            investment_income=request.investment_income,
            rmd_income=Decimal(str(proj["rmd_income"])),
            other_income=request.other_income,
            adjusted_gross_income=Decimal(str(proj["magi"])),
            magi=Decimal(str(proj["magi"])),
            irmaa_tier=proj["irmaa_tier"],
            monthly_premium_surcharge=Decimal(str(proj["monthly_surcharge"])),
            annual_premium_surcharge=Decimal(str(proj["annual_surcharge"])),
        )
        session.add(db_proj)

    session.commit()

    return {
        "user_id": user_id,
        "forecast_id": forecast_id,
        "projections": projections,
    }


@router.get("/irmaa/user/{user_id}")
def get_user_irmaa_projections(
    user_id: int,
    forecast_id: Optional[int] = None,
    session: Session = Depends(get_session),
):
    """Get IRMAA projections for a user"""
    query = select(IRMAAProjection).where(IRMAAProjection.user_id == user_id)

    if forecast_id:
        query = query.where(IRMAAProjection.forecast_id == forecast_id)

    projections = session.exec(query).all()

    return {
        "user_id": user_id,
        "forecast_id": forecast_id,
        "projections": [
            {
                "year": p.year,
                "age": p.age,
                "magi": float(p.magi),
                "irmaa_tier": p.irmaa_tier,
                "monthly_surcharge": float(p.monthly_premium_surcharge),
                "annual_surcharge": float(p.annual_premium_surcharge),
            }
            for p in projections
        ],
    }


@router.get("/user/{user_id}/tax-bucket-summary")
def get_user_tax_bucket_summary(user_id: int, session: Session = Depends(get_session)):
    """Get summary of all tax buckets across all accounts for retirement planning"""

    # Get all accounts for user (would need to join through accounts table)
    from ..models.account import Account
    accounts = session.exec(select(Account).where(Account.user_id == user_id)).all()

    summary = {
        "user_id": user_id,
        "total_pre_tax": Decimal("0.00"),
        "total_roth": Decimal("0.00"),
        "total_after_tax": Decimal("0.00"),
        "total_taxable": Decimal("0.00"),
        "accounts": [],
    }

    for account in accounts:
        buckets = session.exec(
            select(InvestmentTaxBucket).where(InvestmentTaxBucket.account_id == account.id),
        ).all()

        account_summary = {
            "account_id": account.id,
            "account_name": account.name,
            "buckets": [],
        }

        for bucket in buckets:
            account_summary["buckets"].append(
                {
                    "tax_classification": bucket.tax_classification,
                    "balance": float(bucket.balance),
                },
            )

            # Add to totals
            if bucket.tax_classification == "pre_tax":
                summary["total_pre_tax"] += bucket.balance
            elif bucket.tax_classification == "roth":
                summary["total_roth"] += bucket.balance
            elif bucket.tax_classification == "after_tax":
                summary["total_after_tax"] += bucket.balance
            elif bucket.tax_classification == "taxable":
                summary["total_taxable"] += bucket.balance

        if account_summary["buckets"]:
            summary["accounts"].append(account_summary)

    # Convert Decimal to float for JSON response
    summary["total_pre_tax"] = float(summary["total_pre_tax"])
    summary["total_roth"] = float(summary["total_roth"])
    summary["total_after_tax"] = float(summary["total_after_tax"])
    summary["total_taxable"] = float(summary["total_taxable"])
    summary["total_all"] = (
            summary["total_pre_tax"] +
            summary["total_roth"] +
            summary["total_after_tax"] +
            summary["total_taxable"]
    )

    return summary
