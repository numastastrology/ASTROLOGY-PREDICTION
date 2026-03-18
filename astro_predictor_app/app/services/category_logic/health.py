from astro_predictor_app.app.utils.astro_utils import (
    get_sign_number, get_sign_name, get_planet_sign, calculate_house, get_lord,
    get_planet_nature, get_house_outcome, get_ordinal, get_dignity,
    analyze_planetary_aspects, analyze_transits, analyze_jamakkol, analyze_dasa_bhukti_detailed
)
from astro_predictor_app.app.utils.remedy_utils import get_general_remedies, get_dasa_remedies
from astro_predictor_app.app.utils.description_utils import LAGNA_HOUSE_INDICATORS

def analyze(birth_details, chart_data, dasa_info=None):
    points = []
    asc_sign = chart_data.get('ascendant', '')
    planetary_pos = chart_data.get('planetary_positions', {})
    transit_pos = chart_data.get('transit_positions', {})
    jamakkol_data = chart_data.get('jamakkol', {})
    
    # Target Houses for Health: 1 (Vitality), 6 (Disease), 8 (Longevity), 12 (Hospitalization)
    target_houses = [1, 6, 8, 12]
    
    base_score = 70
    
    # 1. Foundation
    h1_sign = asc_sign
    h1_lord = get_lord(h1_sign)
    points.append(f"<b>Vitality Foundation:</b> Your physical constitution is governed by <b>{h1_sign}</b> energy and <b>{h1_lord}</b> influences.")

    if asc_sign in LAGNA_HOUSE_INDICATORS:
        # Filter for health specific indicators
        all_indicators = LAGNA_HOUSE_INDICATORS[asc_sign].get("General", [])
        health_indicators = [i for i in all_indicators if any(keyword in i.lower() for keyword in ["health", "vitality", "body", "physical"])]
        points.extend(health_indicators)

    # 2. Key Significator (Sun for Vitality)
    sun_pos = planetary_pos.get('Sun', '')
    s_sign = get_planet_sign(sun_pos)
    s_house = calculate_house(s_sign, asc_sign)
    s_dignity = get_dignity('Sun', s_sign)
    points.append(f"<b>Vitality Significator:</b> Sun is in the {get_ordinal(s_house)} house in <b>{s_sign}</b>.")
    points.append(f"<b>Overall Energy:</b> Sun triggers <b>{get_house_outcome(s_house, type='pos' if s_dignity != 'Debilitated' else 'neg', category='Health')}</b> in your life.")

    if s_dignity == 'Debilitated':
        base_score -= 10
        points.append("<b>Challenge:</b> Sun is restricted, suggesting a need for consistent focus on building immunity and stamina.")
    elif s_dignity == 'Exalted':
        base_score += 10
        points.append("<b>Strength:</b> Sun is powerful, providing strong natural vitality and recuperative powers.")

    # 3. House-by-House Impacts
    area_map = {
        6: "Resistance & Debts",
        8: "Longevity & Transformation",
        12: "Rest & Rejuvenation"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                  nature = get_planet_nature(planet)
                  # In health, malefic in 6 can be good for defeating diseases
                  is_positive = planet in ['Jupiter', 'Venus'] or (house_num == 6 and planet in ['Mars', 'Saturn', 'Rahu'])
                  outcome = get_house_outcome(house_num, type='pos' if is_positive else 'neg', category='Health')
                  points.append(f"<b>{area}:</b> {planet}'s presence brings <b>{nature}</b> here, triggering <b>{outcome}</b>.")
                  if not is_positive and house_num != 6: base_score -= 5
                  found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers <b>{get_house_outcome(house_num, category='Health')}</b>.")

    # 4. Strategic Advice
    advice = "Maintain a balanced lifestyle with regular exercise and a nutritional diet to preserve your natural vitality."
    if base_score < 60:
        advice = "Prioritize preventative health check-ups and stress management techniques."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses, category='Health'))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses, category='Health'))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses, category='Health'))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Health"))

    # --- Dynamic Health Synthesis ---
    from astro_predictor_app.app.utils.astro_utils import get_dynamic_recommendations
    dynamic_insights = get_dynamic_recommendations(planetary_pos, asc_sign, 'Health')

    points.append("<b>Key Health & Vitality Insights:</b>")
    
    lagna_recs = []
    # Combine and limit
    combined_recs = dynamic_insights + lagna_recs
    final_recs = []
    seen = set()
    for r in combined_recs:
        if r and r not in seen:
            final_recs.append(r)
            seen.add(r)
            if len(final_recs) >= 5: break

    for rec in final_recs:
        points.append(f"• {rec}")

    # Remedies Integration
    remedies = get_general_remedies("health")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
