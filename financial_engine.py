from pydantic import BaseModel

class FinancialRequest(BaseModel):
    margin_capital: float
    business_category: str

def calculate_financial_terms(req: FinancialRequest) -> dict:
    margin_capital = req.margin_capital
    # Standard promoter margin assumption is ~15% - 20%
    total_project_cost = margin_capital * 5
    eligible_loan_amount = total_project_cost - margin_capital
    
    category_lower = req.business_category.lower()
    
    # Scheme, interest, and tenure matching based on business category
    if any(k in category_lower for k in ["dairy", "poultry", "pisciculture", "fish"]):
        scheme_name = "NABARD / Animal Husbandry Scheme"
        interest_rate_percent = 7.5
        tenure_years = 7
        moratorium_months = 12
    elif any(k in category_lower for k in ["agro", "oil", "textile", "mill", "processing"]):
        scheme_name = "PMEGP / Stand-Up India"
        interest_rate_percent = 8.5
        tenure_years = 5
        moratorium_months = 6
    else:
        scheme_name = "MUDRA Scheme (Tarun/Kishore)"
        interest_rate_percent = 9.0
        tenure_years = 5
        moratorium_months = 3

    # Reducing balance quarterly EMI calculation
    r = (interest_rate_percent / 100) / 4
    n = tenure_years * 4
    if r > 0 and n > 0:
        quarterly_installment = round((eligible_loan_amount * r * ((1 + r) ** n)) / (((1 + r) ** n) - 1))
    else:
        quarterly_installment = round(eligible_loan_amount / max(n, 1))

    return {
        "scheme_name": scheme_name,
        "interest_rate_percent": interest_rate_percent,
        "tenure_years": tenure_years,
        "moratorium_months": moratorium_months,
        "margin_capital": margin_capital,
        "eligible_loan_amount": eligible_loan_amount,
        "total_project_cost": total_project_cost,
        "quarterly_installment": quarterly_installment
    }
