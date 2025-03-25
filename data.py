from models import WaterSource, HistoricalData, QualityPrediction, Metric, Disease
from typing import List, Dict

water_sources: List[WaterSource] = [
    WaterSource(
        id="source1",
        name="Gaborone Dam",
        location="South East",
        type="Dam",
        metrics=[
            Metric(id="ph", name="pH Level", value=7.2, unit="", safeRange=[6.5, 8.5], status="safe", icon="beaker"),
            Metric(id="turbidity", name="Turbidity", value=1.3, unit="NTU", safeRange=[0, 5], status="safe", icon="droplet"),
            Metric(id="chlorine", name="Chlorine", value=1.8, unit="mg/L", safeRange=[0.2, 4], status="safe", icon="beaker"),
            Metric(id="bacteria", name="Bacteria Count", value=15, unit="CFU/100mL", safeRange=[0, 100], status="safe", icon="bug"),
            Metric(id="lead", name="Lead", value=8, unit="ppb", safeRange=[0, 15], status="warning", icon="alert-circle"),
            Metric(id="nitrate", name="Nitrate", value=4.2, unit="mg/L", safeRange=[0, 10], status="safe", icon="beaker")
        ],
        diseases=[
            Disease(id="disease1", name="Gastrointestinal Illness", riskLevel="low", description="Conditions that affect the digestive system, causing nausea, vomiting, and diarrhea.", causedBy=["bacteria", "parasites"]),
            Disease(id="disease2", name="Lead Poisoning", riskLevel="medium", description="Lead exposure can cause developmental issues, particularly in children and pregnant women.", causedBy=["lead"])
        ]
    ),
    WaterSource(
        id="source2",
        name="Notwane River",
        location="South East",
        type="River",
        metrics=[
            Metric(id="ph", name="pH Level", value=6.8, unit="", safeRange=[6.5, 8.5], status="safe", icon="beaker"),
            Metric(id="turbidity", name="Turbidity", value=4.7, unit="NTU", safeRange=[0, 5], status="warning", icon="droplet"),
            Metric(id="chlorine", name="Chlorine", value=0.5, unit="mg/L", safeRange=[0.2, 4], status="safe", icon="beaker"),
            Metric(id="bacteria", name="Bacteria Count", value=210, unit="CFU/100mL", safeRange=[0, 100], status="danger", icon="bug"),
            Metric(id="lead", name="Lead", value=2, unit="ppb", safeRange=[0, 15], status="safe", icon="alert-circle"),
            Metric(id="nitrate", name="Nitrate", value=12, unit="mg/L", safeRange=[0, 10], status="danger", icon="beaker")
        ],
        diseases=[
            Disease(id="disease1", name="Gastrointestinal Illness", riskLevel="high", description="Conditions that affect the digestive system, causing nausea, vomiting, and diarrhea.", causedBy=["bacteria", "parasites"]),
            Disease(id="disease3", name="Blue Baby Syndrome", riskLevel="medium", description="A condition caused by high nitrate levels in water that affects infants, reducing oxygen in the bloodstream.", causedBy=["nitrate"]),
            Disease(id="disease4", name="Giardiasis", riskLevel="medium", description="A diarrheal disease caused by the parasite Giardia, often found in untreated river water.", causedBy=["parasites"])
        ]
    ),
    WaterSource(
        id="source3",
        name="Shashe Dam",
        location="Central",
        type="Dam",
        metrics=[
            Metric(id="ph", name="pH Level", value=8.1, unit="", safeRange=[6.5, 8.5], status="warning", icon="beaker"),
            Metric(id="turbidity", name="Turbidity", value=0.8, unit="NTU", safeRange=[0, 5], status="safe", icon="droplet"),
            Metric(id="chlorine", name="Chlorine", value=0.1, unit="mg/L", safeRange=[0.2, 4], status="danger", icon="beaker"),
            Metric(id="bacteria", name="Bacteria Count", value=5, unit="CFU/100mL", safeRange=[0, 100], status="safe", icon="bug"),
            Metric(id="lead", name="Lead", value=1, unit="ppb", safeRange=[0, 15], status="safe", icon="alert-circle"),
            Metric(id="nitrate", name="Nitrate", value=7.5, unit="mg/L", safeRange=[0, 10], status="warning", icon="beaker")
        ],
        diseases=[
            Disease(id="disease5", name="Bacterial Infections", riskLevel="low", description="Various infections caused by bacteria in inadequately treated water.", causedBy=["bacteria", "low chlorine"])
        ]
    )
]

historical_data: List[HistoricalData] = [
    HistoricalData(metricId="ph", metricName="pH Level", data=[{"date": "2023-01", "value": 7.1}, {"date": "2023-02", "value": 7.2}, {"date": "2023-03", "value": 7.0}, {"date": "2023-04", "value": 7.3}, {"date": "2023-05", "value": 7.4}, {"date": "2023-06", "value": 7.2}]),
    HistoricalData(metricId="turbidity", metricName="Turbidity", data=[{"date": "2023-01", "value": 1.8}, {"date": "2023-02", "value": 1.5}, {"date": "2023-03", "value": 2.1}, {"date": "2023-04", "value": 1.7}, {"date": "2023-05", "value": 1.4}, {"date": "2023-06", "value": 1.3}]),
    HistoricalData(metricId="bacteria", metricName="Bacteria Count", data=[{"date": "2023-01", "value": 25}, {"date": "2023-02", "value": 30}, {"date": "2023-03", "value": 18}, {"date": "2023-04", "value": 22}, {"date": "2023-05", "value": 16}, {"date": "2023-06", "value": 15}])
]

quality_predictions: Dict[str, QualityPrediction] = {
    "source1": QualityPrediction(score=85, status="Good", description="The water quality is generally good with only minor concerns about lead levels. Safe for most uses with monitoring.", improvementSteps=["Continue monitoring lead levels", "Maintain current treatment protocols", "Schedule regular infrastructure checks"]),
    "source2": QualityPrediction(score=58, status="Fair", description="Several concerning parameters including high bacteria and nitrate levels. Additional treatment recommended.", improvementSteps=["Increase chlorination treatment", "Implement nitrate reduction measures", "Install additional filtration systems", "Monitor upstream agricultural activities"]),
    "source3": QualityPrediction(score=75, status="Good", description="Generally safe water with concerns about low chlorine levels that could affect disinfection.", improvementSteps=["Adjust chlorine dosing system", "Monitor pH levels to keep within optimal range", "Continue regular testing protocols"])
}
