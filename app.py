from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from feasibility_engine import generate_hyperlocal_feasibility, FeasibilityRequest
from financial_engine import calculate_financial_terms, FinancialRequest

app = FastAPI(
    title="Rural Fintech Engine",
    description="API for hyper-local feasibility analysis and financial structuring.",
    version="1.0.0"
)

# Enable CORS so Netlify and any client domain can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EnterpriseAssessmentRequest(BaseModel):
    state: str
    district: str
    block: str
    margin_capital: float
    business_category: str

@app.get("/")
def health_check():
    return {
        "status": "online",
        "service": "Rural Fintech Engine API",
        "docs_url": "/docs"
    }

@app.post("/api/v1/assess-enterprise")
def assess_enterprise(req: EnterpriseAssessmentRequest):
    try:
        # 1. Compute financial structuring based on margin capital and business sector
        fin_req = FinancialRequest(
            margin_capital=req.margin_capital,
            business_category=req.business_category
        )
        financial_data = calculate_financial_terms(fin_req)

        # 2. Extract total project cost and generate hyper-local feasibility
        total_project_cost = financial_data.get("total_project_cost", req.margin_capital * 10)
        feas_req = FeasibilityRequest(
            state=req.state,
            district=req.district,
            block=req.block,
            business_category=req.business_category,
            total_project_cost=total_project_cost
        )
        feasibility_data = generate_hyperlocal_feasibility(feas_req)

        return {
            "feasibility_report": feasibility_data,
            "financial_structuring": financial_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
