from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class BirthDetails(BaseModel):
    name: str
    date_of_birth: str  # Format: YYYY-MM-DD
    time_of_birth: str  # Format: HH:MM
    place_of_birth: str
    latitude: float
    longitude: float
    timezone: float
    star: Optional[str] = None
    pada: Optional[int] = None
    manual_dasa: Optional[Dict[str, str]] = None # {"dasa_lord": "Rahu", "bhukti_lord": "Venus", "antara_lord": "Saturn", "dasa_end_date": "2025-01-01"}

class Profile(BirthDetails):
    id: Optional[str] = None  # Unique ID for storage

class PredictionRequest(BaseModel):
    birth_details: BirthDetails
    selected_categories: Optional[List[str]] = None  # If None, select all by default

class PredictionResponse(BaseModel):
    status: str
    chart_summary: Dict[str, Any]
    predictions: Dict[str, Dict[str, Any]]  # Changed to Dict containing 'points' (List[str]) and 'score' (int)

class ReportRequest(BaseModel):
    prediction_data: PredictionResponse
    selected_categories: Optional[List[str]] = None
