import sys
import os
from datetime import datetime

# Add the app directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from astro_predictor_app.app.services.category_logic.native import analyze as analyze_native
from astro_predictor_app.app.services.category_logic.education import analyze as analyze_education
from astro_predictor_app.app.services.category_logic.career import analyze as analyze_career

def test_diverse_coverage():
    test_cases = [
        {"name": "Ashwini Start", "asc": "Aries", "moon_sign": "Aries", "star": "Ashwini", "pada": "1"},
        {"name": "Swati Middle", "asc": "Libra", "moon_sign": "Libra", "star": "Swati", "pada": "3"},
        {"name": "Revati End", "asc": "Pisces", "moon_sign": "Pisces", "star": "Revati", "pada": "4"}
    ]
    
    for case in test_cases:
        print(f"\n--- Testing: {case['name']} ---")
        birth_details = type('obj', (object,), {'name': 'Test User'})
        chart_data = {
            "ascendant": case['asc'],
            "planetary_positions": {
                "Moon": case['moon_sign'],
                "Sun": "Aries",
                "Mercury": "Gemini",
                "Jupiter": "Sagittarius",
                "Venus": "Taurus",
                "Saturn": "Capricorn"
            },
            "nakshatra": case['star'],
            "pada": case['pada']
        }
        
        native_res = analyze_native(birth_details, chart_data)
        edu_res = analyze_education(birth_details, chart_data)
        career_res = analyze_career(birth_details, chart_data)
        
        # Simple checks for output presence
        assert native_res and len(native_res['points']) > 0, f"Native analysis failed for {case['name']}"
        assert edu_res and len(edu_res['points']) > 0, f"Education analysis failed for {case['name']}"
        assert career_res and len(career_res['points']) > 0, f"Career analysis failed for {case['name']}"
        
        print(f"Outcome for {case['star']} {case['pada']}: SUCCESS")
        print(f"Sample Native Point: {native_res['points'][0][:100]}...")

if __name__ == "__main__":
    try:
        test_diverse_coverage()
        print("\n✅ ALL DIVERSE TEST CASES PASSED!")
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
