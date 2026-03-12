from fastapi import APIRouter, HTTPException
from astro_predictor_app.app.schemas import BirthDetails
import datetime

router = APIRouter(prefix="/input", tags=["Input Validation"])

@router.post("/validate")
def validate_input(details: BirthDetails):
    """
    Validate birth details formats (simple check).
    Real validation would check if city exists, lat/long are valid, etc.
    """
    try:
        # Validate Date
        datetime.datetime.strptime(details.date_of_birth, "%Y-%m-%d")
        # Validate Time
        datetime.datetime.strptime(details.time_of_birth, "%H:%M")
        
        return {"status": "valid", "message": "Input data is valid"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date or time format: {str(e)}")
