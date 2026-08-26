from pydantic import BaseModel
from typing import Dict, Any, List

class FinancialRequest(BaseModel):
    margin_capital: float  
    business_category: str

class FinancialOutput(BaseModel):
    total_project_cost: float
    eligible_loan_amount: float
    scheme_name: str
    interest_rate_percent: float
    tenure_years: int
    moratorium_months: int
    quarterly_installment: float
    total_repayment: float
    total_interest: float
    schedule: List[Dict[str, Any]]

def calculate_loan_structure(data: FinancialRequest) -> FinancialOutput:
    project_cost = data.margin_capital / 0.10
    eligible_loan = project_cost * 0.90

    if project_cost <= 140000:
        scheme_name = "Micro Finance Scheme"
        eligible_loan = min(eligible_loan, 125000) 
        annual_rate = 0.065  
        tenure_years = 3
        moratorium_months = 3
    elif project_cost <= 5000000:
        scheme_name = "Term Loan Scheme"
        eligible_loan = min(eligible_loan, 4500000) 
        annual_rate = 0.08  
        tenure_years = 7
        moratorium_months = 6
    else:
        raise ValueError("Project cost exceeds the ₹50.00 Lakh maximum limit.")

    total_quarters = tenure_years * 4
    moratorium_quarters = moratorium_months // 3
    repayment_quarters = total_quarters - moratorium_quarters

    quarterly_rate = annual_rate / 4
    
    q_emi = eligible_loan * (
        (quarterly_rate * (1 + quarterly_rate) ** repayment_quarters)
        / (((1 + quarterly_rate) ** repayment_quarters) - 1)
    )

    balance = eligible_loan
    schedule = []
    total_interest = 0.0

    for q in range(1, moratorium_quarters + 1):
        schedule.append({
            "quarter": q, "payment": 0.0, "principal": 0.0,
            "interest": 0.0, "balance": round(balance, 2), "status": "Moratorium"
        })

    for q in range(moratorium_quarters + 1, total_quarters + 1):
        interest_for_q = balance * quarterly_rate
        principal_for_q = q_emi - interest_for_q
        balance -= principal_for_q
        total_interest += interest_for_q
        
        schedule.append({
            "quarter": q, "payment": round(q_emi, 2), "principal": round(principal_for_q, 2),
            "interest": round(interest_for_q, 2), "balance": max(0.0, round(balance, 2)),
            "status": "Active Repayment"
        })

    return FinancialOutput(
        total_project_cost=round(project_cost, 2), eligible_loan_amount=round(eligible_loan, 2),
        scheme_name=scheme_name, interest_rate_percent=annual_rate * 100, tenure_years=tenure_years,
        moratorium_months=moratorium_months, quarterly_installment=round(q_emi, 2),
        total_repayment=round(eligible_loan + total_interest, 2), total_interest=round(total_interest, 2),
        schedule=schedule
    )