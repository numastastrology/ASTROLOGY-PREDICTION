from astro_predictor_app.app.schemas import BirthDetails
from astro_predictor_app.app.services.astrology_engine import astrology_engine
import sys

def test_native_category():
    # Sample Birth Data (User's specific case mentioned in history or generic)
    # Using generic data for test
    bd = BirthDetails(
        name="TestUser",
        date_of_birth="1990-01-01",
        time_of_birth="10:00",
        place_of_birth="Chennai, India",
        latitude=13.0827,
        longitude=80.2707,
        timezone=5.5
    )

    print("Calculating chart...")
    chart_data = astrology_engine.calculate_chart(bd)
    if "error" in chart_data:
        print(f"Chart Error: {chart_data['error']}")
        sys.exit(1)

    print("Generating predictions with filtered categories...")
    # Simulate API behavior where user selects 'career' but we expect 'native_characteristics' to be forced
    filtered_cats = ["career"]
    if "native_characteristics" not in filtered_cats:
        filtered_cats.append("native_characteristics") # Logic we added to prediction.py

    all_predictions = astrology_engine.generate_all_predictions(
        bd, 
        chart_data,
        selected_categories=filtered_cats
    )

    if "native_characteristics" not in all_predictions:
        print("FAIL: 'native_characteristics' category missing from predictions.")
        sys.exit(1)

    native_data = all_predictions["native_characteristics"]
    points = native_data.get("points", [])
    
    print(f"\n--- Native Category Output ({len(points)} points) ---")
    for i, p in enumerate(points):
        print(f"{i+1}. {p}")

    if len(points) < 20:
        print(f"\nFAIL: Expected 20+ points, got {len(points)}")
        sys.exit(1)
    
    print("\nSUCCESS: Native category generated with sufficient points.")

if __name__ == "__main__":
    test_native_category()
