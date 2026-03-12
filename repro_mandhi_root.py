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
    
    print(f"Calculating chart for {details.date_of_birth} {details.time_of_birth}")
    chart = astrology_engine.calculate_chart(details)
    
    print("Mandhi Position (Rasi):", chart['planetary_positions'].get('Mandhi'))
    print("Mandhi Position (Navamsa):", chart['navamsa_positions'].get('Mandhi'))
    print("Ascendant (Navamsa):", chart['navamsa_ascendant'])
    print("Jamakkol:", chart.get('jamakkol'))

if __name__ == "__main__":
    test_mandhi()
