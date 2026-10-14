"""Tests for financial service."""

import pytest
from app.services import financial_service


def test_calculate_project_cost():
    """Test project cost calculation."""
    # Available margin is 10% of project cost
    assert financial_service.calculate_project_cost(100000) == 1000000
    assert financial_service.calculate_project_cost(50000) == 500000
    assert financial_service.calculate_project_cost(200000) == 2000000


def test_calculate_project_cost_invalid():
    """Test project cost with invalid inputs."""
    with pytest.raises(ValueError):
        financial_service.calculate_project_cost(0)

    with pytest.raises(ValueError):
        financial_service.calculate_project_cost(-1000)


def test_calculate_loan_amount():
    """Test loan amount calculation."""
    # Loan is 90% of project cost
    assert financial_service.calculate_loan_amount(1000000) == 900000
    assert financial_service.calculate_loan_amount(500000) == 450000
    assert financial_service.calculate_loan_amount(2000000) == 1800000


def test_select_scheme_micro_finance():
    """Test Micro Finance Scheme selection."""
    # Project cost <= 1.40 lakh
    scheme = financial_service.select_scheme(140000)
    assert scheme["scheme_name"] == "Micro Finance Scheme"
    assert scheme["interest_rate"] == 6.5
    assert scheme["tenure_years"] == 3
    assert scheme["moratorium_months"] == 3


def test_select_scheme_term_loan():
    """Test Term Loan Scheme selection."""
    # 1.40 lakh < project cost <= 50 lakh
    scheme = financial_service.select_scheme(500000)
    assert scheme["scheme_name"] == "Term Loan Scheme"
    assert scheme["interest_rate"] == 8.0
    assert scheme["tenure_years"] == 7
    assert scheme["moratorium_months"] == 6

    scheme = financial_service.select_scheme(5000000)
    assert scheme["scheme_name"] == "Term Loan Scheme"


def test_select_scheme_out_of_range():
    """Test scheme selection with out of range project cost."""
    # Project cost > 50 lakh should raise error
    with pytest.raises(ValueError, match="exceeds the maximum supported limit"):
        financial_service.select_scheme(6000000)


def test_calculate_emi():
    """Test EMI calculation."""
    # Test with typical values
    emi = financial_service.calculate_emi(
        loan_amount=900000,
        annual_rate=8.0,
        tenure_years=7,
        moratorium_months=6
    )
    assert emi > 0
    assert isinstance(emi, float)

    # EMI should be reasonable (not too high or too low)
    assert 10000 < emi < 20000


def test_calculate_emi_zero_loan():
    """Test EMI with zero loan amount."""
    emi = financial_service.calculate_emi(0, 8.0, 7, 6)
    assert emi == 0


def test_calculate_financials_complete():
    """Test complete financial calculation."""
    result = financial_service.calculate_financials(200000)

    assert result["available_margin_capital"] == 200000
    assert result["project_cost"] == 2000000
    assert result["maximum_loan"] == 1800000
    assert result["scheme_name"] == "Term Loan Scheme"
    assert result["interest_rate"] == 8.0
    assert result["tenure_years"] == 7
    assert result["moratorium_months"] == 6
    assert result["emi"] > 0
    assert len(result["repayment_schedule"]) == 84  # 7 years * 12 months


def test_calculate_financials_micro_finance():
    """Test financial calculation for Micro Finance range."""
    result = financial_service.calculate_financials(10000)

    assert result["project_cost"] == 100000
    assert result["maximum_loan"] == 90000
    assert result["scheme_name"] == "Micro Finance Scheme"
    assert result["interest_rate"] == 6.5
    assert result["tenure_years"] == 3


def test_generate_repayment_schedule():
    """Test repayment schedule generation."""
    schedule = financial_service.generate_repayment_schedule(
        loan_amount=900000,
        annual_rate=8.0,
        tenure_years=7,
        moratorium_months=6
    )

    assert len(schedule) == 84  # 7 years * 12 months

    # Check first month (moratorium)
    assert schedule[0]["month"] == 1
    assert schedule[0]["payment"] == 0
    assert schedule[0]["principal"] == 0
    assert schedule[0]["interest"] > 0

    # Check after moratorium
    assert schedule[6]["month"] == 7
    assert schedule[6]["payment"] > 0
    assert schedule[6]["principal"] > 0

    # Check last month
    assert schedule[-1]["month"] == 84
    assert schedule[-1]["balance"] >= 0  # Should be paid off or near zero
