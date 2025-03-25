# models.py
from pydantic import BaseModel
from typing import List, Dict

class Disease(BaseModel):
    id: str
    name: str
    riskLevel: str
    description: str
    causedBy: List[str]

class Metric(BaseModel):
    id: str
    name: str
    value: float
    unit: str
    safeRange: List[float]
    status: str
    icon: str

class WaterSource(BaseModel):
    id: str
    name: str
    location: str
    type: str
    metrics: List[Metric]
    diseases: List[Disease]

class QualityPrediction(BaseModel):
    score: int
    status: str
    description: str
    improvementSteps: List[str]

class HistoricalData(BaseModel):
    metricId: str
    metricName: str
    data: List[dict] 


class HistoricalDataItem(BaseModel):
    date: str
    value: float 