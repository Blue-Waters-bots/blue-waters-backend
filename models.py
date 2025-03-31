# models.py
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import uuid

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

class Alert(BaseModel):
    id: str
    message: str
    source: str
    level: str
    metric: str
    value: float
    unit: str
    timestamp: datetime

    def __init__(self, **data):
        if 'id' not in data:
            data['id'] = str(uuid.uuid4()) 
        super().__init__(**data)

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