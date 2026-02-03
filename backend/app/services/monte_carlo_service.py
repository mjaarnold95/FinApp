"""
Monte Carlo simulation service for retirement forecasting
"""
from decimal import Decimal
from typing import List, Dict, Tuple

import numpy as np


class MonteCarloSimulator:
    """Monte Carlo simulation for retirement planning"""

    def __init__(
        self,
        current_age: int,
        retirement_age: int,
        life_expectancy: int,
        current_savings: Decimal,
        annual_contribution: Decimal,
        annual_withdrawal: Decimal,
        expected_return: Decimal,
        volatility: Decimal,
        inflation_rate: Decimal = Decimal("2.5"),
        num_simulations: int = 10000,
    ):
        self.current_age = current_age
        self.retirement_age = retirement_age
        self.life_expectancy = life_expectancy
        self.current_savings = float(current_savings)
        self.annual_contribution = float(annual_contribution)
        self.annual_withdrawal = float(annual_withdrawal)
        self.expected_return = float(expected_return) / 100.0
        self.volatility = float(volatility) / 100.0
        self.inflation_rate = float(inflation_rate) / 100.0
        self.num_simulations = num_simulations

        self.years_to_retirement = retirement_age - current_age
        self.years_in_retirement = life_expectancy - retirement_age
        self.total_years = life_expectancy - current_age

    def run_simulation(self) -> Dict:
        """Run Monte Carlo simulation"""
        results = []
        final_balances = []

        for i in range(self.num_simulations):
            balance_path = self._simulate_single_path()
            results.append(balance_path)
            final_balances.append(balance_path[-1])

        # Calculate success rate (how many simulations didn't run out of money)
        successful_sims = sum(1 for bal in final_balances if bal > 0)
        success_rate = (successful_sims / self.num_simulations) * 100

        # Calculate percentiles
        final_balances_sorted = sorted(final_balances)
        median_balance = final_balances_sorted[len(final_balances_sorted) // 2]
        p10_balance = final_balances_sorted[int(len(final_balances_sorted) * 0.10)]
        p90_balance = final_balances_sorted[int(len(final_balances_sorted) * 0.90)]

        # Calculate year-by-year statistics
        year_stats = self._calculate_year_stats(results)

        return {
            "success_rate": Decimal(str(round(success_rate, 2))),
            "median_final_balance": Decimal(str(round(median_balance, 2))),
            "percentile_10_balance": Decimal(str(round(max(0, p10_balance), 2))),
            "percentile_90_balance": Decimal(str(round(p90_balance, 2))),
            "num_simulations": self.num_simulations,
            "year_stats": year_stats,
        }

    def _simulate_single_path(self) -> List[float]:
        """Simulate a single retirement path"""
        balance = self.current_savings
        path = [balance]

        for year in range(self.total_years):
            age = self.current_age + year

            # Generate random return for this year
            random_return = np.random.normal(self.expected_return, self.volatility)

            # Apply return
            balance *= (1 + random_return)

            # Add contributions during working years
            if age < self.retirement_age:
                # Adjust contribution for inflation
                inflated_contribution = self.annual_contribution * ((1 + self.inflation_rate) ** year)
                balance += inflated_contribution

            # Subtract withdrawals during retirement
            if age >= self.retirement_age:
                years_in_retirement = age - self.retirement_age
                # Adjust withdrawal for inflation
                inflated_withdrawal = self.annual_withdrawal * (
                            (1 + self.inflation_rate) ** (self.years_to_retirement + years_in_retirement))
                balance -= inflated_withdrawal

            # Balance cannot go negative
            balance = max(0, balance)
            path.append(balance)

            # If balance hits zero, it stays zero
            if balance == 0:
                break

        # Fill remaining years with zeros if ran out early
        while len(path) < self.total_years + 1:
            path.append(0)

        return path

    def _calculate_year_stats(self, results: List[List[float]]) -> List[Dict]:
        """Calculate statistics for each year across all simulations"""
        year_stats = []

        for year_idx in range(self.total_years + 1):
            balances_this_year = [sim[year_idx] for sim in results if year_idx < len(sim)]
            balances_sorted = sorted(balances_this_year)

            year_stats.append(
                {
                    "year": year_idx,
                    "age": self.current_age + year_idx,
                    "median": round(balances_sorted[len(balances_sorted) // 2], 2),
                    "p10": round(balances_sorted[int(len(balances_sorted) * 0.10)], 2),
                    "p90": round(balances_sorted[int(len(balances_sorted) * 0.90)], 2),
                    "min": round(min(balances_this_year), 2),
                    "max": round(max(balances_this_year), 2),
                },
            )

        return year_stats


class RMDCalculator:
    """Calculate Required Minimum Distributions"""

    # IRS Uniform Lifetime Table (2024+)
    LIFE_EXPECTANCY_TABLE = {
        72: 27.4, 73: 26.5, 74: 25.5, 75: 24.6, 76: 23.7, 77: 22.9, 78: 22.0, 79: 21.1,
        80: 20.2, 81: 19.4, 82: 18.5, 83: 17.7, 84: 16.8, 85: 16.0, 86: 15.2, 87: 14.4,
        88: 13.7, 89: 12.9, 90: 12.2, 91: 11.5, 92: 10.8, 93: 10.1, 94: 9.5, 95: 8.9,
        96: 8.4, 97: 7.8, 98: 7.3, 99: 6.8, 100: 6.4, 101: 6.0, 102: 5.6, 103: 5.2,
        104: 4.9, 105: 4.6, 106: 4.3, 107: 4.1, 108: 3.9, 109: 3.7, 110: 3.5, 111: 3.4,
        112: 3.3, 113: 3.1, 114: 3.0, 115: 2.9, 116: 2.8, 117: 2.7, 118: 2.5, 119: 2.3,
        120: 2.0,
    }

    @staticmethod
    def calculate_rmd(age: int, account_balance: Decimal) -> Tuple[Decimal, Decimal]:
        """
        Calculate RMD for a given age and balance
        
        Note: RMD age varies by birth year under SECURE 2.0:
        - Age 73 for those born 1951-1959
        - Age 75 for those born 1960 or later
        
        Returns:
            Tuple of (rmd_amount, life_expectancy_factor)
        """
        if age < 73:  # Minimum RMD age (may vary by birth year)
            return Decimal("0.00"), Decimal("0.00")

        # Get life expectancy from IRS table
        life_expectancy = RMDCalculator.LIFE_EXPECTANCY_TABLE.get(age)

        if life_expectancy is None:
            if age > 120:
                life_expectancy = 2.0  # Use minimum for very old ages
            else:
                # Age is below minimum table age (72), should not calculate RMD
                return Decimal("0.00"), Decimal("0.00")

        rmd_amount = account_balance / Decimal(str(life_expectancy))
        return rmd_amount, Decimal(str(life_expectancy))

    @staticmethod
    def project_rmds(
        starting_age: int,
        ending_age: int,
        pre_tax_balance: Decimal,
        expected_return: Decimal,
        additional_withdrawals: Decimal = Decimal("0.00"),
    ) -> List[Dict]:
        """
        Project RMDs over multiple years
        
        Returns:
            List of dicts with year, age, balance, and rmd_amount
        """
        projections = []
        balance = pre_tax_balance
        return_rate = float(expected_return) / 100.0

        for age in range(starting_age, ending_age + 1):
            # Calculate RMD for this year
            rmd_amount, life_exp = RMDCalculator.calculate_rmd(age, balance)
            total_withdrawal = rmd_amount + additional_withdrawals

            projections.append(
                {
                    "year": age - starting_age,
                    "age": age,
                    "account_balance": float(balance),
                    "rmd_amount": float(rmd_amount),
                    "life_expectancy_factor": float(life_exp),
                    "total_withdrawal": float(total_withdrawal),
                },
            )

            # Update balance for next year
            balance -= total_withdrawal
            balance *= Decimal(str(1 + return_rate))
            balance = max(Decimal("0.00"), balance)

        return projections


class IRMAACalculator:
    """Calculate IRMAA (Income-Related Monthly Adjustment Amount) for Medicare"""

    # 2024 IRMAA brackets (single filer)
    IRMAA_BRACKETS_SINGLE = [
        {"max_magi": 103000, "tier": "standard", "part_b_surcharge": 0, "part_d_surcharge": 0},
        {"max_magi": 129000, "tier": "tier1", "part_b_surcharge": 69.90, "part_d_surcharge": 12.20},
        {"max_magi": 161000, "tier": "tier2", "part_b_surcharge": 174.70, "part_d_surcharge": 31.50},
        {"max_magi": 193000, "tier": "tier3", "part_b_surcharge": 279.50, "part_d_surcharge": 50.70},
        {"max_magi": 500000, "tier": "tier4", "part_b_surcharge": 384.30, "part_d_surcharge": 70.00},
        {"max_magi": float('inf'), "tier": "tier5", "part_b_surcharge": 419.30, "part_d_surcharge": 76.40},
    ]

    # 2024 IRMAA brackets (married filing jointly)
    IRMAA_BRACKETS_MARRIED = [
        {"max_magi": 206000, "tier": "standard", "part_b_surcharge": 0, "part_d_surcharge": 0},
        {"max_magi": 258000, "tier": "tier1", "part_b_surcharge": 69.90, "part_d_surcharge": 12.20},
        {"max_magi": 322000, "tier": "tier2", "part_b_surcharge": 174.70, "part_d_surcharge": 31.50},
        {"max_magi": 386000, "tier": "tier3", "part_b_surcharge": 279.50, "part_d_surcharge": 50.70},
        {"max_magi": 750000, "tier": "tier4", "part_b_surcharge": 384.30, "part_d_surcharge": 70.00},
        {"max_magi": float('inf'), "tier": "tier5", "part_b_surcharge": 419.30, "part_d_surcharge": 76.40},
    ]

    @staticmethod
    def calculate_irmaa(magi: Decimal, filing_status: str = "single") -> Dict:
        """
        Calculate IRMAA surcharge based on MAGI
        
        Args:
            magi: Modified Adjusted Gross Income
            filing_status: "single" or "married"
            
        Returns:
            Dict with tier, monthly and annual surcharges
        """
        brackets = (IRMAACalculator.IRMAA_BRACKETS_MARRIED
                    if filing_status == "married"
                    else IRMAACalculator.IRMAA_BRACKETS_SINGLE)

        magi_float = float(magi)

        for bracket in brackets:
            if magi_float <= bracket["max_magi"]:
                monthly_surcharge = bracket["part_b_surcharge"] + bracket["part_d_surcharge"]
                return {
                    "tier": bracket["tier"],
                    "part_b_monthly": Decimal(str(bracket["part_b_surcharge"])),
                    "part_d_monthly": Decimal(str(bracket["part_d_surcharge"])),
                    "monthly_total": Decimal(str(monthly_surcharge)),
                    "annual_total": Decimal(str(monthly_surcharge * 12)),
                }

        # Shouldn't reach here, but return highest tier as fallback
        return {
            "tier": "tier5",
            "monthly_total": Decimal("495.70"),
            "annual_total": Decimal("5948.40"),
        }

    @staticmethod
    def project_irmaa(
        starting_age: int,
        ending_age: int,
        income_sources: Dict[str, Decimal],
        rmd_projections: List[Dict],
        filing_status: str = "single",
    ) -> List[Dict]:
        """
        Project IRMAA costs over retirement years
        
        Args:
            starting_age: Age to start projections
            ending_age: Age to end projections
            income_sources: Dict of income sources (social_security, pension, investment_income, etc.)
            rmd_projections: List of RMD projections from RMDCalculator
            filing_status: "single" or "married"
            
        Returns:
            List of IRMAA projections by year
        """
        projections = []

        for age in range(starting_age, ending_age + 1):
            # Find RMD for this age
            rmd_income = Decimal("0.00")
            for rmd_proj in rmd_projections:
                if rmd_proj["age"] == age:
                    rmd_income = Decimal(str(rmd_proj["rmd_amount"]))
                    break

            # Calculate total income (MAGI approximation)
            total_income = (
                    income_sources.get("social_security", Decimal("0.00")) +
                    income_sources.get("pension", Decimal("0.00")) +
                    income_sources.get("investment_income", Decimal("0.00")) +
                    rmd_income +
                    income_sources.get("other_income", Decimal("0.00"))
            )

            # Calculate IRMAA
            irmaa_result = IRMAACalculator.calculate_irmaa(total_income, filing_status)

            projections.append(
                {
                    "year": age - starting_age,
                    "age": age,
                    "magi": float(total_income),
                    "rmd_income": float(rmd_income),
                    "irmaa_tier": irmaa_result["tier"],
                    "monthly_surcharge": float(irmaa_result["monthly_total"]),
                    "annual_surcharge": float(irmaa_result["annual_total"]),
                },
            )

        return projections
