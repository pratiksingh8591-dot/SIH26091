"""Financial service for project cost, loan, scheme routing, and EMI calculations."""

from __future__ import annotations

from typing import Any, Dict, List


def calculate_project_cost(available_margin: float) -> float:
    """Calculate project cost from available margin capital.

    The available margin represents 10% of the total project cost.
    Formula: project_cost = available_margin / 0.10

    Args:
        available_margin: Available margin capital in rupees

    Returns:
        Project cost in rupees

    Raises:
        ValueError: If available_margin is negative or zero
    """
    if available_margin <= 0:
        raise ValueError("Available margin capital must be greater than zero")

    return available_margin / 0.10


def calculate_loan_amount(project_cost: float) -> float:
    """Calculate maximum loan amount from project cost.

    Formula: loan_amount = project_cost * 0.90

    Args:
        project_cost: Total project cost in rupees

    Returns:
        Maximum loan amount in rupees
    """
    return project_cost * 0.90


def select_scheme(project_cost: float) -> Dict[str, Any]:
    """Select appropriate financial scheme based on project cost.

    Rules:
    - If project_cost <= ₹1.40 lakh:
        Scheme: Micro Finance Scheme
        Interest: 6.5% per annum
        Tenure: 3 years
        Moratorium: 3 months

    - If ₹1.40 lakh < project_cost <= ₹50 lakh:
        Scheme: Term Loan Scheme
        Interest: 8% per annum
        Tenure: 7 years
        Moratorium: 6 months

    - If project_cost > ₹50 lakh:
        Unsupported range (error)

    Args:
        project_cost: Total project cost in rupees

    Returns:
        Dict with scheme_name, interest_rate, tenure_years, moratorium_months

    Raises:
        ValueError: If project cost is outside supported range
    """
    # Convert to lakhs for easier comparison
    project_cost_lakhs = project_cost / 100000

    if project_cost_lakhs <= 1.40:
        return {
            "scheme_name": "Micro Finance Scheme",
            "interest_rate": 6.5,
            "tenure_years": 3,
            "moratorium_months": 3,
        }
    elif project_cost_lakhs <= 50.0:
        return {
            "scheme_name": "Term Loan Scheme",
            "interest_rate": 8.0,
            "tenure_years": 7,
            "moratorium_months": 6,
        }
    else:
        raise ValueError(
            f"Project cost of ₹{project_cost:,.2f} (₹{project_cost_lakhs:.2f} lakh) "
            "exceeds the maximum supported limit of ₹50 lakh"
        )


def calculate_emi(
    loan_amount: float,
    annual_rate: float,
    tenure_years: int,
    moratorium_months: int,
) -> float:
    """Calculate EMI using reducing balance method.

    EMI starts after the moratorium period.
    Formula: EMI = [P * r * (1 + r)^n] / [(1 + r)^n - 1]
    where:
        P = loan principal
        r = monthly interest rate (annual_rate / 12 / 100)
        n = number of months

    Args:
        loan_amount: Principal loan amount in rupees
        annual_rate: Annual interest rate (e.g., 6.5 for 6.5%)
        tenure_years: Loan tenure in years
        moratorium_months: Moratorium period in months

    Returns:
        Monthly EMI amount in rupees
    """
    if loan_amount <= 0:
        return 0.0

    # Monthly interest rate
    monthly_rate = annual_rate / 12 / 100

    # Total months excluding moratorium
    total_months = tenure_years * 12
    repayment_months = total_months - moratorium_months

    if repayment_months <= 0:
        return 0.0

    # EMI formula: [P * r * (1 + r)^n] / [(1 + r)^n - 1]
    if monthly_rate == 0:
        emi = loan_amount / repayment_months
    else:
        power_term = (1 + monthly_rate) ** repayment_months
        emi = (loan_amount * monthly_rate * power_term) / (power_term - 1)

    return round(emi, 2)


def generate_repayment_schedule(
    loan_amount: float,
    annual_rate: float,
    tenure_years: int,
    moratorium_months: int,
) -> List[Dict[str, Any]]:
    """Generate monthly repayment schedule.

    During moratorium: only interest is accumulated
    After moratorium: EMI payments with principal and interest breakdown

    Args:
        loan_amount: Principal loan amount in rupees
        annual_rate: Annual interest rate
        tenure_years: Loan tenure in years
        moratorium_months: Moratorium period in months

    Returns:
        List of monthly payment dicts with month, principal, interest, balance
    """
    schedule = []
    balance = loan_amount
    monthly_rate = annual_rate / 12 / 100
    total_months = tenure_years * 12

    emi = calculate_emi(loan_amount, annual_rate, tenure_years, moratorium_months)

    for month in range(1, total_months + 1):
        if month <= moratorium_months:
            # Moratorium period: only interest accrues
            interest = balance * monthly_rate
            principal = 0.0
            payment = 0.0  # No payment during moratorium
            balance += interest  # Interest is added to principal
        else:
            # Regular EMI period
            interest = balance * monthly_rate
            principal = emi - interest
            payment = emi
            balance -= principal

            # Ensure balance doesn't go negative due to rounding
            if balance < 0:
                balance = 0

        schedule.append(
            {
                "month": month,
                "payment": round(payment, 2),
                "principal": round(principal, 2),
                "interest": round(interest, 2),
                "balance": round(balance, 2),
            }
        )

    return schedule


def calculate_financials(available_margin_capital: float) -> Dict[str, Any]:
    """Calculate complete financial analysis from margin capital.

    This is the main function that ties together all financial calculations.

    Args:
        available_margin_capital: Available margin capital in rupees

    Returns:
        Dict with all financial details including project cost, loan, scheme, EMI, schedule

    Raises:
        ValueError: If inputs are invalid or project cost is unsupported
    """
    if available_margin_capital <= 0:
        raise ValueError("Available margin capital must be greater than zero")

    # Calculate project cost
    project_cost = calculate_project_cost(available_margin_capital)

    # Calculate loan amount
    loan_amount = calculate_loan_amount(project_cost)

    # Select scheme
    try:
        scheme = select_scheme(project_cost)
    except ValueError as e:
        raise ValueError(str(e))

    # Calculate EMI
    emi = calculate_emi(
        loan_amount,
        scheme["interest_rate"],
        scheme["tenure_years"],
        scheme["moratorium_months"],
    )

    # Generate repayment schedule
    repayment_schedule = generate_repayment_schedule(
        loan_amount,
        scheme["interest_rate"],
        scheme["tenure_years"],
        scheme["moratorium_months"],
    )

    return {
        "available_margin_capital": round(available_margin_capital, 2),
        "project_cost": round(project_cost, 2),
        "maximum_loan": round(loan_amount, 2),
        "scheme_name": scheme["scheme_name"],
        "interest_rate": scheme["interest_rate"],
        "tenure_years": scheme["tenure_years"],
        "moratorium_months": scheme["moratorium_months"],
        "emi": emi,
        "repayment_schedule": repayment_schedule,
    }
