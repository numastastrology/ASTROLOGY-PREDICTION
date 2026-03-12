from fastapi import APIRouter
from fastapi.responses import FileResponse
from astro_predictor_app.app.schemas import ReportRequest
from astro_predictor_app.app.utils.pdf_generator import generate_prediction_report
import os
from astro_predictor_app.config.settings import settings

router = APIRouter(prefix="/report", tags=["Reports"])

@router.post("/generate_pdf")
def generate_report(request: ReportRequest):
    """
    Generate a PDF report based on the provided prediction data.
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(settings.PDF_OUTPUT_DIR):
        os.makedirs(settings.PDF_OUTPUT_DIR)
        
    filename = f"report_{request.prediction_data.chart_summary.get('name', 'user')}.pdf"
    filepath = os.path.join(settings.PDF_OUTPUT_DIR, filename)
    
    # Check if there are select categories to filter the report content
    selected_categories = request.selected_categories
    if selected_categories:
        # Filter the predictions in the report request data
        all_preds = request.prediction_data.predictions
        # Ensure 'native_characteristics' is always included if available, even if not in selected_categories
        filtered_preds = {k: v for k, v in all_preds.items() if k in selected_categories or k == "native_characteristics"}
        request.prediction_data.predictions = filtered_preds

    try:
        # Generate PDF
        actual_filepath = generate_prediction_report(
            request.prediction_data.model_dump(), 
            filepath
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Return a 500 with details (optional, but good for debugging)
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"PDF Generation Failed: {str(e)}")
    
    return FileResponse(actual_filepath, media_type='application/pdf', filename=filename)
