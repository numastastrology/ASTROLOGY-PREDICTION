import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from astro_predictor_app.app.services.astrology_engine import astrology_engine
from astro_predictor_app.app.schemas import BirthDetails

def test_mandhi():
    details = BirthDetails(
        name="SAMPLE REPORT",
        date_of_birth="2009-04-09",
        time_of_birth="22:58:00",
        place_of_birth="Chengalpattu, Tamil Nadu, India",
        latitude=12.6936,
        longitude=79.9769,
        timezone=5.5
    )
    
    chart = astrology_engine.calculate_chart(details)
    
    print("Mandhi Position (Rasi):", chart['planetary_positions'].get('Mandhi'))
    print("Mandhi Position (Navamsa):", chart['navamsa_positions'].get('Mandhi'))
    print("Ascendant (Navamsa):", chart['navamsa_ascendant'])

if __name__ == "__main__":
    test_mandhi()
