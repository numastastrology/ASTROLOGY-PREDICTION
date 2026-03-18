
import sys
import os
from datetime import datetime

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from astro_predictor_app.app.schemas import BirthDetails
from astro_predictor_app.app.services.astrology_engine import astrology_engine

def debug_aries_prediction():
    # Use birth details that definitely give Aries Lagna, Taurus Moon, and Rohini Nakshatra
    # For testing, I'll just MOCK the calculate_chart output if necessary, 
    # but let's try to see what's being passed.
    bd = BirthDetails(
        name="R KANNAN",
        date_of_birth="1972-03-23",
        time_of_birth="09:00",
        place_of_birth="Bengaluru",
        latitude=12.9767936,
        longitude=77.590082,
        timezone=5.5
    )

    print("Calculating chart...")
    chart_data = astrology_engine.calculate_chart(bd)
    print(f"Lagna: {chart_data['ascendant']}")
    print(f"Nakshatra: {chart_data['nakshatra']} (Pada {chart_data['pada']})")
    print(f"Moon: {chart_data['planetary_positions'].get('Moon', 'Unknown')}")

    # No manual overrides this time!
    # chart_data['ascendant'] = "Aries"
    # chart_data['nakshatra'] = "Rohini"
    # ...

    print("\nGenerating all predictions...")
    predictions = astrology_engine.generate_all_predictions(bd, chart_data)
    
    if "native_characteristics" in predictions:
        print("\n--- Native Characteristics Points ---")
        for p in predictions["native_characteristics"]["points"]:
            print(f"- {p}")
            if "Athletic build" in p:
                print(">>> FOUND: Lagna trait found!")
            if "Calm, steady" in p:
                print(">>> FOUND: Moon trait found!")
    else:
        print("FAIL: native_characteristics missing!")

    if "education" in predictions:
        print("\n--- Education Points ---")
        for p in predictions["education"]["points"]:
            if "2nd House (Gemini)" in p:
                print(f"- {p}")
                print(">>> FOUND: Education indicator!")

    if "career" in predictions:
        print("\n--- Career Points ---")
        for p in predictions["career"]["points"]:
            if "Top Career Recommendations" in p:
                print(f"- {p}")
                print(">>> FOUND: Career recommendations!")

    print("\nGenerating PDF Report...")
    from astro_predictor_app.app.utils.pdf_generator import generate_prediction_report
    from astro_predictor_app.app.schemas import PredictionResponse
    
    # Mocking PredictionResponse structure for the generator
    full_data = {
        "status": "success",
        "chart_summary": chart_data,
        "predictions": predictions
    }
    
    pdf_filename = "debug_aries_report.pdf"
    generate_prediction_report(full_data, pdf_filename)
    print(f"SUCCESS: {pdf_filename} generated.")

if __name__ == "__main__":
    debug_aries_prediction()
