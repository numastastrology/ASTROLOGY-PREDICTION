
from astro_predictor_app.app.services.category_logic.career import analyze

# Mock data simulating a chart with strong Mercury in 10th (Aquarius Lagna)
# 10th house for Aquarius is Scorpio (Mars ruler).
# But if Mercury is in 10th or 11th, it should give Finance/Accounts.

mock_chart = {
    'ascendant': 'Aquarius',
    'planetary_positions': {
        'Mercury': 'Scorpio', # 10th house
        'Jupiter': 'Sagittarius', # 11th house (Exalted/Own)
        'Saturn': 'Aquarius' # 1st house (Own)
    },
    'nakshatra': 'Ardra',
    'pada': 1,
    'jamakkol': {},
    'transit_positions': {}
}

result = analyze({}, mock_chart)
print("Points:")
for p in result['points']:
    if "Top Recommended Career Paths" in p or "•" in p:
        print(p)
