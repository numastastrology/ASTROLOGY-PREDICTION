import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from astro_predictor_app.app.services.category_logic import (
    relationships, children, career, finance, health, 
    luck_factor, native, dasa_predictions, business_vs_job
)

# S KARTIK Birth Data (Simulated for testing)
birth_data = {
    "name": "S KARTIK",
    "dob": "1979-12-05",
    "tob": "13:16:00",
    "lat": 13.0836939,
    "lon": 80.270186,
    "tz": 5.5
}

# Chart Data for S KARTIK (Aquarius ASC)
chart_data = {
    "ascendant": "Aquarius",
    "planetary_positions": {
        "Sun": "Scorpio (10th)",
        "Moon": "Taurus (4th)",
        "Mars": "Leo (7th)",
        "Mercury": "Scorpio (10th)",
        "Jupiter": "Leo (7th)",
        "Venus": "Sagittarius (11th)",
        "Saturn": "Virgo (8th)",
        "Rahu": "Leo (7th)",
        "Ketu": "Aquarius (1st)"
    },
    "transit_positions": {
        "Jupiter": "Taurus",
        "Saturn": "Aquarius",
        "Ketu": "Leo"
    },
    "jamakkol": {
        "udayam": "Capricorn (12th)",
        "kavippu": "Cancer (6th)"
    }
}

dasa_info = {
    "dasa": {"lord": "Saturn", "end": "2030-10-26"},
    "bhukti": {"lord": "Rahu", "end": "2028-04-13"},
    "antara": {"lord": "Jupiter", "end": "2026-03-29"}
}

categories = {
    "Relationships": relationships,
    "Children": children,
    "Career": career,
    "Finance": finance,
    "Health": health,
    "Luck Factor": luck_factor,
    "Native": native,
    "Dasa Predictions": dasa_predictions,
    "Business vs Job": business_vs_job
}

print("=== COMPREHENSIVE SCORING VERIFICATION (PLAIN ENGLISH) ===")
for name, module in categories.items():
    result = module.analyze(birth_data, chart_data, dasa_info)
    print(f"\n--- {name} Analysis ---")
    print(f"Score: {result['score']}%")
    print("Key Points:")
    for point in result['points']:
        # For Dasa Predictions or Points with <b>, show them
        if name == "Dasa Predictions" or "<b>" in point:
             # Strip HTML tags for clean terminal output if needed, but keeping for verification of tags
             print(f"  * {point}")
    
    if name == "Dasa Predictions":
        print(f"Total Points: {len(result['points'])}")

print("\nVerification Complete.")
