from astro_predictor_app.app.utils.astro_utils import (
    get_sign_number, get_sign_name, get_planet_sign, calculate_house, get_lord,
    get_planet_nature, get_house_outcome, get_ordinal, get_dignity,
    analyze_planetary_aspects, analyze_transits, analyze_jamakkol, analyze_dasa_bhukti_detailed
)
from astro_predictor_app.app.utils.remedy_utils import get_general_remedies, get_dasa_remedies

def analyze(birth_details, chart_data, dasa_info=None):
    points = []
    asc_sign = chart_data.get('ascendant', '')
    planetary_pos = chart_data.get('planetary_positions', {})
    transit_pos = chart_data.get('transit_positions', {})
    jamakkol_data = chart_data.get('jamakkol', {})
    
    # Target Houses for Challenges: 8 (Sudden obstacles), 12 (Losses), 6 (Obstacles)
    target_houses = [8, 12, 6]
    
    base_score = 60
    
    # 1. Foundation
    h8_sign = get_sign_name((get_sign_number(asc_sign) + 8 - 1) % 12 or 12)
    h8_lord = get_lord(h8_sign)
    points.append(f"<b>Challenge Foundation:</b> Your path through sudden obstacles is influenced by <b>{h8_sign}</b> energy, governed by <b>{h8_lord}</b> influences.")

    # 2. Key Significator (Saturn for Karma/Delays)
    saturn_pos = planetary_pos.get('Saturn', '')
    s_house = calculate_house(get_planet_sign(saturn_pos), asc_sign)
    if s_house in [6, 8, 12]:
         points.append(f"<b>Karmic influence:</b> Saturn in the {get_ordinal(s_house)} house suggests obstacles are linked to long-term lessons.")

    # 3. House-by-House Impacts
    area_map = {
        8: "Sudden Changes",
        12: "Unseen Losses",
        6: "Physical Hurdles"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                  nature = get_planet_nature(planet)
                  outcome = get_house_outcome(house_num, type='neg', category='Health')
                  points.append(f"<b>{area}:</b> {planet}'s presence brings <b>{nature}</b> here, triggering <b>{outcome}</b>.")
                  found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers <b>{get_house_outcome(house_num, category='Health', type='neg')}</b>.")

    # 4. Strategic Advice
    advice = "Maintain a steady routine and focus on spiritual grounding to navigate through challenging periods."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses, category='Health'))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses, category='Health'))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses, category='Health'))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Challenges & Obstacles"))

    # Remedies Integration
    remedies = get_general_remedies("health") # Generic remedies for challenges
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
