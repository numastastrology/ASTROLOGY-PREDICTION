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
    
    # Target Houses for Family: 2 (Family), 4 (Home), 11 (Social Circle)
    target_houses = [2, 4, 11]
    
    base_score = 70
    
    # 1. Foundation
    h2_sign = get_sign_name((get_sign_number(asc_sign) + 2 - 1) % 12 or 12)
    h2_lord = get_lord(h2_sign)
    points.append(f"<b>Family Foundation:</b> Your domestic environment is influenced by <b>{h2_sign}</b> energy, governed by <b>{h2_lord}</b> influences.")

    # 2. Key Significator (Jupiter for Family Wisdom, Moon for Emotions)
    jupiter_pos = planetary_pos.get('Jupiter', '')
    j_house = calculate_house(get_planet_sign(jupiter_pos), asc_sign)
    if j_house in [2, 4, 9]:
         points.append(f"<b>Family Wisdom:</b> Jupiter in the {get_ordinal(j_house)} house provides a strong moral and emotional anchor for the family.")

    # 3. House-by-House Impacts
    area_map = {
        2: "Family Continuity",
        4: "Home Environment",
        11: "Wider Circle"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                  nature = get_planet_nature(planet)
                  outcome = get_house_outcome(house_num, type='pos' if planet in ['Jupiter', 'Venus', 'Moon'] else 'neg', category='Relationships')
                  points.append(f"<b>{area}:</b> {planet}'s presence brings <b>{nature}</b> here, triggering <b>{outcome}</b>.")
                  found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers <b>{get_house_outcome(house_num, category='Relationships')}</b>.")

    # 4. Strategic Advice
    advice = "Maintain transparency and emotional bonding to ensure a harmonious domestic life."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses, category='Relationships'))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses, category='Relationships'))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses, category='Relationships'))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Family & Domestic Life"))

    # Remedies Integration
    remedies = get_general_remedies("relationships") # Use relationship remedies for family harmony
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
