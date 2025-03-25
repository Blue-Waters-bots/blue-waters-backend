from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
from models import WaterSource, HistoricalData, QualityPrediction
from data import water_sources, historical_data, quality_predictions

app = FastAPI(
    title="Blue Waters Backend",
    description="Backend for Blue Waters Dashboard",
    version="1.0.0",
)

# Allow CORS for your frontend URL
origins = [
    "http://localhost:8080",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)


water_quality_responses: Dict[str, str] = {
    "What are the recommended actions if the nitrate level exceeds 10 ppm?": 
    """If the nitrate level exceeds 10 ppm, the recommended actions depend on the industry:
    
    - **Mining**: This is not directly applicable as mining operations typically deal with heavy metals rather than nitrates.
    - **Water Treatment Plants**: If nitrate levels are high, it may indicate contamination from agricultural runoff or sewage. Additional filtration methods, such as reverse osmosis or ion exchange, may be necessary to reduce nitrate levels.
    - **Water Utilities**: High nitrate levels can pose a risk to public health, especially for infants. The utility should consider implementing additional treatment processes, such as biological nitrification/denitrification, ion exchange, or reverse osmosis.
    - **Agriculture**: High nitrate levels in irrigation water can lead to excessive plant growth and potential toxicity in crops. Recommendations include switching to alternative water sources, implementing proper irrigation practices, and possibly using nitrate-reducing bacteria to lower nitrate levels.
    
    In all cases, it's crucial to identify the source of the high nitrate levels and address it to prevent future contamination.""",

    "Is water with 20 mg/L nitrate safe to drink?": 
    """Water with 20 mg/L nitrate does not meet the EPA's maximum contaminant level (MCL) for nitrate, which is 10 mg/L for drinking water. 
    High nitrate levels can pose health risks, particularly for infants under six months old, as nitrate can convert to nitrite in the stomach, potentially leading to methemoglobinemia, also known as blue baby syndrome.""",

    "Our water has a dissolved oxygen level of 2 mg/L. Is this acceptable for mining operations?":
    """The acceptable dissolved oxygen level for mining operations can vary depending on the specific mining process and the type of minerals being extracted. However, generally, dissolved oxygen levels below 5 mg/L can indicate poor water quality and potential issues with aquatic life or corrosion in mining equipment."""
}

health_risk_responses: Dict[str, str] = {
    "What are the health risks of consuming water with high arsenic levels?": 
    """Long-term exposure to high arsenic levels in drinking water can cause serious health problems, including:
    
    - **Cancer**: Increased risk of bladder, lung, and skin cancer.
    - **Skin Lesions**: Thickening and dark spots on the skin.
    - **Cardiovascular Issues**: Increased risk of high blood pressure and heart disease.
    - **Neurological Effects**: Can lead to memory problems and impaired cognitive function.
    - **Developmental Issues**: Children exposed to arsenic may experience developmental problems.

    The EPA's maximum contaminant level (MCL) for arsenic in drinking water is **0.010 mg/L**. If arsenic levels exceed this limit, consider installing an **arsenic filtration system** or switching to a **safer water source**.""",

    "How does high lead contamination in water affect health?": 
    """Lead contamination in drinking water can have severe health effects, especially for children and pregnant women. Health risks include:
    
    - **Neurological Damage**: Lead exposure can impair brain development in children, leading to learning disabilities and reduced IQ.
    - **Kidney Damage**: Long-term exposure can cause kidney failure.
    - **High Blood Pressure**: Lead can contribute to cardiovascular diseases.
    - **Behavioral Issues**: Children exposed to lead may experience hyperactivity, aggression, and attention disorders.

    The EPA's action level for lead in drinking water is **0.015 mg/L**. If water tests show lead contamination, consider **installing lead-removing filters**, replacing old lead pipes, and **flushing taps before use**.""",

    "What are the symptoms of nitrate poisoning from drinking water?":
    """Nitrate poisoning, also known as methemoglobinemia or "blue baby syndrome," can occur when infants consume water with high nitrate levels (above 10 mg/L). Symptoms include:
    
    - **Bluish skin color (cyanosis)**, especially around the mouth and fingertips.
    - **Difficulty breathing** and shortness of breath.
    - **Fatigue, dizziness, and headaches** due to reduced oxygen levels in the blood.
    - **Rapid heartbeat**.
    - **Loss of consciousness in severe cases**.

    If you suspect nitrate poisoning, seek **immediate medical attention** and switch to **low-nitrate drinking water** (e.g., bottled or treated water).""",

    "I have water with high ph is safe for my cows?":
    """High pH levels in water can affect the health of your cows. While high pH levels do not directly cause immediate harm like high levels of contaminants such as arsenic, nitrates, or lead, they can still have indirect effects on your cattle's health and productivity.

Reduced water intake: Cows prefer water with a pH between 6.0 and 7.0. Water with a high pH (above 7.0) can taste bitter, leading to reduced water intake. This can result in dehydration, which can negatively impact milk production and overall health.
Mineral imbalances: High pH water can lead to mineral imbalances in the cows' bodies. For example, high pH water can cause an increase in sodium and a decrease in calcium and magnesium absorption, which can affect bone health and milk production.
Urinary issues: High pH urine can lead to the formation of struvite (magnesium ammonium phosphate) stones in the urinary tract, causing discomfort and potential blockages.
To ensure the health of your cows, it is recommended to test the water regularly and, if necessary, implement measures to adjust the pH levels. This can be done by adding small amounts of an acid, such as sulfuric or hydrochloric acid, to lower the pH. However, it is crucial to consult with a livestock expert or a water quality specialist before making any adjustments to ensure the safety and effectiveness of the process."""
}

@app.get("/water-sources", response_model=List[WaterSource])
async def get_water_sources():
    return water_sources

@app.get("/water-source/{source_id}", response_model=WaterSource)
async def get_water_source_by_id(source_id: str):
    source = next((source for source in water_sources if source.id == source_id), None)
    if source is None:
        raise HTTPException(status_code=404, detail="Water source not found")
    return source

@app.get("/historical-data", response_model=List[HistoricalData])
async def get_historical_data():
    return historical_data

@app.get("/quality-predictions/{source_id}", response_model=QualityPrediction)
async def get_quality_prediction(source_id: str):
    prediction = quality_predictions.get(source_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction

# Simulate AI Agent Responses
@app.get("/simulate-water-quality-agent")
async def simulate_water_quality_agent(query: str = Query(..., description="Enter your query related to water quality")):
    response = water_quality_responses.get(query, "I'm sorry, I don't have an answer for that.")
    return {"response": response}

# Simulate Health Advisory Agent
@app.get("/simulate-health-risk-agent")
async def simulate_health_risk_agent(query: str = Query(..., description="Enter your query related to health risks")):
    response = health_risk_responses.get(query, "I'm sorry, I don't have an answer for that.")
    return {"response": response}

