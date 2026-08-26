import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class FeasibilityRequest(BaseModel):
    state: str
    district: str
    block: str
    business_category: str
    total_project_cost: float

def generate_hyperlocal_feasibility(req: FeasibilityRequest) -> dict:
    model = genai.GenerativeModel('gemini-3.5-flash')
    
    prompt = f"""
You are an expert institutional rural micro-enterprise consultant and economic data analyst.
Generate a rigorous, empirically grounded hyper-local feasibility analysis for:
- Exact Target Location: {req.block}, District: {req.district}, State: {req.state}
- Sector: {req.business_category}
- Feasible Budget / Project Cost: ₹{req.total_project_cost}

CRITICAL INSTRUCTION FOR METRICS & DEMOGRAPHICS:
Do NOT use estimated, nominal, or rounded numbers (avoid multiples of 5 like 40% or 25%). Base your demographic distribution metrics on precise micro-economic indicators, local occupation censuses, and consumer purchasing power tiers typical for '{req.block}'. Provide exact decimal percentages (e.g., 42.3%, 31.7%, 26.0%) that sum up strictly to 100%.

Return your response strictly as a JSON object matching this exact schema without any markdown formatting:
{{
  "demographics": [
    {{"name": "<Target Consumer Group 1>", "percentage": <float precision number, e.g. 42.3>}},
    {{"name": "<Target Consumer Group 2>", "percentage": <float precision number, e.g. 31.7>}},
    {{"name": "<Target Consumer Group 3>", "percentage": <float precision number, e.g. 26.0>}}
  ],
  "channels": [
    {{"name": "<Channel 1>", "viability": "<High, Medium, or Low>"}},
    {{"name": "<Channel 2>", "viability": "<High, Medium, or Low>"}},
    {{"name": "<Channel 3>", "viability": "<High, Medium, or Low>"}}
  ],
  "market_insight": "<One sentence summary of reach based on budget in this exact location>",
  "competitors": {{
    "direct": {{"count": <integer>, "desc": "<short description>", "level": "<High, Medium, or Low>"}},
    "indirect": {{"count": <integer>, "desc": "<short description>", "level": "<High, Medium, or Low>"}}
  }},
  "threat_insight": "<One sentence summary of the biggest market threat in {req.block}>",
  "swot": {{
    "strengths": ["<point 1>", "<point 2>"],
    "weaknesses": ["<point 1>", "<point 2>"],
    "opportunities": ["<point 1>", "<point 2>"],
    "threats": ["<point 1>", "<point 2>"]
  }},
  "local_risks": [
    {{"title": "<Risk 1 title>", "desc": "<Detailed risk description specific to {req.block}>", "level": "<High or Medium>"}}
  ],
  "niches": [
    {{"title": "<Niche 1 title>", "desc": "<Description>", "demand": "<High or Medium>", "competition": "<Low or Medium>"}}
  ],
  "statistical_pricing": {{
    "unit": "<e.g., per Liter, per Kg, per Service>",
    "market_minimum": <integer lowest price competitors charge>,
    "market_maximum": <integer highest price premium market will pay>,
    "optimal_price": <integer mathematically ideal price for volume>
  }},
  "pricing_tip": "<One actionable pricing tip for {req.block}>"
}}
"""
    response = model.generate_content(prompt)
    raw_content = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(raw_content)