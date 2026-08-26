from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import traceback

from financial_engine import calculate_loan_structure, FinancialRequest, FinancialOutput
from feasibility_engine import generate_hyperlocal_feasibility, FeasibilityRequest

app = FastAPI(title="Hyper-Local Business Advisory API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Added 'state' to the request model
class FullAssessmentRequest(BaseModel):
    state: str
    district: str
    block: str
    village: str = ""
    margin_capital: float
    business_category: str
    language: str = "en"

@app.post("/api/v1/assess-enterprise")
def assess_enterprise(req: FullAssessmentRequest):
    try:
        fin_req = FinancialRequest(margin_capital=req.margin_capital, business_category=req.business_category)
        fin_data = calculate_loan_structure(fin_req)

        # Passed 'state' into the feasibility engine
        feasibility_req = FeasibilityRequest(
            state=req.state,
            district=req.district, 
            block=req.block, 
            business_category=req.business_category, 
            total_project_cost=fin_data.total_project_cost
        )
        feasibility_data = generate_hyperlocal_feasibility(feasibility_req)

        return {
            "financial_structuring": fin_data.dict(),
            "feasibility_report": feasibility_data
        }
    except Exception as e:
        print("\n🚨 ERROR TRIGGERED 🚨")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)