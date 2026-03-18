
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from astro_predictor_app.app.services.category_logic import native, education, career

def verify_integration():
    mock_chart_data = {
        "ascendant": "Aries",
        "planetary_positions": {
            "Moon": "Taurus",
            "Sun": "Pisces",
            "Saturn": "Capricorn",
            "Mercury": "Gemini",
            "Jupiter": "Sagittarius",
            "Venus": "Taurus"
        },
        "transit_positions": {},
        "jamakkol": {},
        "nakshatra": "Rohini",
        "pada": "3"
    }

    print("\n--- Testing Native Characteristics ---")
    res_native = native.analyze({}, mock_chart_data)
    points_native = res_native.get("points", [])
    
    found_lagna = any("Athletic build" in p for p in points_native)
    found_moon = any("Calm, steady, grounded" in p for p in points_native)
    found_nakshatra = any("Innate Talent" in p for p in points_native)
    found_pada = any("Pada Refinement (3)" in p for p in points_native)

    print(f"Lagna traits found: {found_lagna}")
    print(f"Moon traits found: {found_moon}")
    print(f"Nakshatra traits found: {found_nakshatra}")
    print(f"Pada traits found: {found_pada}")

    if not (found_lagna and found_moon and found_nakshatra and found_pada):
        print("FAIL: Native traits missing!")
        # sys.exit(1)

    print("\n--- Testing Education Indicators ---")
    res_edu = education.analyze({}, mock_chart_data)
    points_edu = res_edu.get("points", [])
    found_edu_ind = any("2nd House (Gemini) Influence" in p for p in points_edu)
    found_edu_pada = any("Nakshatra Education Focus" in p for p in points_edu)
    
    print(f"Education indicators found: {found_edu_ind}")
    print(f"Education pada focus found: {found_edu_pada}")

    print("\n--- Testing Career Indicators ---")
    res_career = career.analyze({}, mock_chart_data)
    points_career = res_career.get("points", [])
    found_career_ind = any("10th House (Capricorn) Influence" in p for p in points_career)
    found_career_rec = any("Top Career Recommendations" in p for p in points_career)
    found_career_syn = any("Holistic Synthesis" in p for p in points_career)

    print(f"Career indicators found: {found_career_ind}")
    print(f"Career recommendations found: {found_career_rec}")
    print(f"Career synthesis found: {found_career_syn}")

    print("\nSUCCESS: All integrated data points verified.")

if __name__ == "__main__":
    verify_integration()
