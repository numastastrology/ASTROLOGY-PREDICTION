
try:
    from astro_predictor_app.app.utils.description_utils import LAGNA_TRAITS, MOON_TRAITS, NAKSHATRA_TRAITS, PADA_TRAITS
    print("SUCCESS: description_utils imported correctly.")
    print(f"LAGNA_TRAITS: {list(LAGNA_TRAITS.keys())}")
    print(f"MOON_TRAITS: {list(MOON_TRAITS.keys())}")
    print(f"NAKSHATRA_TRAITS: {list(NAKSHATRA_TRAITS.keys())}")
except Exception as e:
    print(f"FAIL: {e}")
