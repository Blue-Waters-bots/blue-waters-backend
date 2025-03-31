from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
from models import WaterSource, HistoricalData, QualityPrediction, Alert
from data import water_sources, historical_data, quality_predictions
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv
from datetime import datetime


# Load environment variables
load_dotenv()

API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_URL = os.getenv("WATSONX_URL")
IAM_URL = "https://iam.cloud.ibm.com/identity/token"
WX_API_BASE_URL = "https://api.dataplatform.cloud.ibm.com"

# Initialize FastAPI
app = FastAPI(
    title="Blue Waters Backend",
    description="Backend for Blue Waters Dashboard",
    version="1.0.0",
)

# Allow CORS for frontend access
origins = ["http://127.0.0.1:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Function to get Bearer Token from IBM WatsonX
def get_bearer_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={API_KEY}"
    
    response = requests.post(IAM_URL, headers=headers, data=data,timeout=(20, 60) )
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print("Bearer Token:", token)  # Print the token for debugging
        return token
    else:
        print("Authentication Error:", response.status_code, response.text)  # Print error details
        raise HTTPException(status_code=500, detail="Failed to authenticate with WatsonX")


def query_watsonx(prompt: str):
    """Query WatsonX AI model with a given prompt dynamically."""
    token = get_bearer_token()  # Make sure this function returns a valid token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "model_id": "ibm/granite-3-8b-instruct",
        "project_id": PROJECT_ID,
        "messages": [
            {
                "role": "system",
                "content": "You are a water quality monitoring assistant. Your job is to analyze water parameters based on EPA standards and provide recommendations."
            },
            {
                "role": "user",
                "content": prompt  # Directly pass the user query as content
            }
        ],
        "max_tokens": 70,
        "temperature": 0.3,
        "time_limit": 1000
    }

    try:
        response = requests.post(f"{WATSONX_URL}/ml/v1/text/chat?version=2023-10-25", json=payload, headers=headers, timeout=300)
        response.raise_for_status()  # Will raise an HTTPError for bad responses

        # Log or print the response for debugging
        print(response.json())

        # Safely extract the AI's response from the "choices" list
        choices = response.json().get("choices", [])
        if choices:
            return choices[0].get("message", {}).get("content", "No response from AI.")
        else:
            return "No response from AI."
    except requests.exceptions.RequestException as e:
        # Handle HTTP or connection errors
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")


# 📌 GET Water Sources
@app.get("/water-sources", response_model=List[WaterSource])
async def get_water_sources():
    return water_sources

# 📌 GET Specific Water Source by ID
@app.get("/water-source/{source_id}", response_model=WaterSource)
async def get_water_source_by_id(source_id: str):
    source = next((source for source in water_sources if source.id == source_id), None)
    if source is None:
        raise HTTPException(status_code=404, detail="Water source not found")
    return source

# 📌 GET Historical Data
@app.get("/historical-data", response_model=List[HistoricalData])
async def get_historical_data():
    return historical_data

# 📌 GET Quality Prediction by Source ID
@app.get("/quality-predictions/{source_id}", response_model=QualityPrediction)
async def get_quality_prediction(source_id: str):
    prediction = quality_predictions.get(source_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction

# 📌 GET Alerts
@app.get("/alerts", response_model=List[Alert])
async def get_alerts():
    # Fetch the latest water sources data
    alerts = []
    for source in water_sources:
        # Check each source for water quality alerts and health risks
        water_quality_alerts = check_water_quality_alerts(source)
        health_risk_alerts = check_health_risk_alerts(source)
        
        alerts.extend(water_quality_alerts)
        alerts.extend(health_risk_alerts)

    return alerts


# Function to check water quality and generate alerts
def check_water_quality_alerts(source: WaterSource) -> List[Alert]:
    alerts = []
    for metric in source.metrics:
        if metric.status == "danger":
            ai_advice = query_watsonx(f"Provide advice for high {metric.name} level ({metric.value} {metric.unit})")
            alert = Alert(
                message=f"{metric.name} is {metric.value} {metric.unit}, which is outside the safe range. Blue Waters AI Advice: {ai_advice}",
                source=source.name,
                level="critical",
                metric=metric.name,
                value=metric.value,
                unit=metric.unit,
                timestamp=datetime.now(),
            )
            alerts.append(alert)
        elif metric.status == "warning":
            ai_advice = query_watsonx(f"Provide advice for warning {metric.name} level ({metric.value} {metric.unit})")
            alert = Alert(
                message=f"{metric.name} is approaching unsafe levels, currently {metric.value} {metric.unit}. Blue Waters AI Advice: {ai_advice}",
                source=source.name,
                level="warning",
                metric=metric.name,
                value=metric.value,
                unit=metric.unit,
                timestamp=datetime.now(),
            )
            alerts.append(alert)
    return alerts


# Function to check health risks and generate alerts
def check_health_risk_alerts(source: WaterSource) -> List[Alert]:
    alerts = []
    for disease in source.diseases:
        if disease.riskLevel == "high":
            ai_advice = query_watsonx(f"Provide advice for high health risk from {disease.name}")
            alert = Alert(
                message=f"Health risk: {disease.name}. This water source poses a high health risk due to {', '.join(disease.causedBy)}. Blue Waters AI Advice: {ai_advice}",
                source=source.name,
                level="critical",
                metric=disease.name,
                value=0,  # Health risk is not a direct value, but a general alert
                unit="",
                timestamp=datetime.now(),
            )
            alerts.append(alert)
        elif disease.riskLevel == "medium":
            ai_advice = query_watsonx(f"Provide advice for medium health risk from {disease.name}")
            alert = Alert(
                message=f"Health risk: {disease.name}. Moderate health risk detected. Take necessary precautions. Blue Waters AI Advice: {ai_advice}",
                source=source.name,
                level="warning",
                metric=disease.name,
                value=0,
                unit="",
                timestamp=datetime.now(),
            )
            alerts.append(alert)
    return alerts


# ✅ AI Agent for Water Quality Advisory (WatsonX Integration)
@app.get("/water-quality-agent")
async def water_quality_agent(query: str = Query(..., description="Enter your query related to water quality")):
    """AI-powered water quality advisory"""
    ai_response = query_watsonx(query)
    return {"response": ai_response}


# ✅ AI Agent for Health Risk Advisory (WatsonX Integration)
@app.get("/health-risk-agent")
async def health_risk_agent(query: str = Query(..., description="Enter your query related to health risks")):
    """AI-powered health risk advisory"""
    ai_response = query_watsonx(query)
    return {"response": ai_response}

# ✅ WatsonX Credentials for Reference (Not used directly in API calls)
credentials = {
    "url": WATSONX_URL,
    "apikey": API_KEY,  
}
