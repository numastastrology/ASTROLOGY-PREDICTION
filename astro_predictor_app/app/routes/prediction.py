from fastapi import APIRouter
from astro_predictor_app.app.schemas import PredictionRequest, PredictionResponse
from astro_predictor_app.app.services.astrology_engine import astrology_engine

router = APIRouter(prefix="/predict", tags=["Predictions"])

@router.post("/generate", response_model=PredictionResponse)
def generate_prediction(request: PredictionRequest):
    """
    Generate predictions based on birth details and selected categories.
    """
    # 1. Calculate Chart
    chart_data = astrology_engine.calculate_chart(request.birth_details)
    
    # 2. Generate Predictions (filtering by selected_categories if provided)
    # Ensure 'native_characteristics' is always generated
    cats = request.selected_categories
    if cats and "native_characteristics" not in cats:
        cats.append("native_characteristics")

    predictions = astrology_engine.generate_all_predictions(
        request.birth_details, 
        chart_data,
        selected_categories=cats
    )
    
    return {
        "status": "success",
        "chart_summary": chart_data,
        "predictions": predictions
    }
