import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from astro_predictor_app.app.services.astrology_engine import astrology_engine
    from astro_predictor_app.app.schemas import BirthDetails
except ImportError:
    # Try adding the subdir if running from parent
    sys.path.append(os.path.join(os.getcwd(), 'astro_predictor_app'))
    from astro_predictor_app.app.services.astrology_engine import astrology_engine
    from astro_predictor_app.app.schemas import BirthDetails

def verify_shift():
    # User requested time correction to 22:59:00
    details = BirthDetails(
        name="SAMPLE REPORT",
        date_of_birth="2009-04-09",
        time_of_birth="22:59:00",
        place_of_birth="Chengalpattu, Tamil Nadu, India",
        latitude=12.6936,
        longitude=79.9769,
        timezone=5.5
    )
    
    print(f"Calculating chart for {details.date_of_birth} {details.time_of_birth}")
    chart = astrology_engine.calculate_chart(details)
    
    # Engine returns:
    # {
    #   "planetary_positions": {...},
    #   "navamsa_positions": {...},
    #   "ascendant": "...",
    #   "navamsa_ascendant": "...",
    #   "nakshatra": "...",
    #   "pada": "..."
    #   "jamakkol": {...}
    # }
    
    print(f"Nakshatra: {chart.get('nakshatra')}")
    print(f"Pada: {chart.get('pada')}")
    print(f"Navamsa Ascendant: {chart.get('navamsa_ascendant')}")
    print(f"Jamakkol: {chart.get('jamakkol')}")
    
    # Run Health Analysis
    from astro_predictor_app.app.services.category_logic import health
    # Mock Dasa info if needed, or extract from chart? 
    # Engine calculates chart but dasa info is usually separate or in 'dasa_details' (not returned by calculate_chart directly?)
    # calculate_chart does NOT return dasa/bhukti info in the dict unless we called generate_predictions.
    # We need to run full prediction generation or mock the input.
    
    # Let's mock Dasa as Rahu/Venus to test the specific missing point
    dasa_mock = {
        "dasa": {"lord": "Rahu", "end": "2030"},
        "bhukti": {"lord": "Venus", "end": "2025"},
        "antara": {"lord": "Saturn", "end": "2024"}
    }
    
    health_res = health.analyze(details, chart, dasa_mock)
    print("\n--- Health Points ---")
    for p in health_res['points']:
        print(f"- {p}")

if __name__ == "__main__":
    verify_shift()
