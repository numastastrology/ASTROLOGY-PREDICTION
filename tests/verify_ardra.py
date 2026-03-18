
import sys
import os
# Add current directory to path
sys.path.append(os.getcwd())

from astro_predictor_app.app.services.category_logic import native, education, career

def test_ardra_integration():
    mock_chart = {
        'ascendant': 'Aries',
        'nakshatra': 'Ardra',
        'pada': 1,
        'planetary_positions': {
            'Moon': 'Gemini',
            'Sun': 'Pisces',
            'Mars': 'Aries',
            'Mercury': 'Gemini',
            'Jupiter': 'Sagittarius',
            'Saturn': 'Libra'
        }
    }
    
    print("\n--- Testing Ardra Native Analysis ---")
    res_native = native.analyze({}, mock_chart)
    found_ardra = any("Ardra" in p for p in res_native['points'])
    found_soul = any("soul's specific direction" in p for p in res_native['points'])
    print(f"Ardra in points: {found_ardra}")
    print(f"Soul explanation in points: {found_soul}")
    for p in res_native['points']:
        if "Ardra" in p or "soul" in p:
            print(f"- {p}")

    print("\n--- Testing Ardra Education/Career ---")
    res_edu = education.analyze({}, mock_chart)
    res_car = career.analyze({}, mock_chart)
    
    found_edu = any("Law, philosophy" in p for p in res_edu['points'])
    found_car = any("Academia, travel industry" in p for p in res_car['points'])
    
    print(f"Education (Law/Philosophy) found: {found_edu}")
    print(f"Career (Academia/Travel) found: {found_car}")

if __name__ == "__main__":
    test_ardra_integration()
