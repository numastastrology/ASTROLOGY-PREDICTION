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
    
    # Target Houses for Debts: 6 (Debts), 12 (Losses), 11 (Gains)
    target_houses = [6, 12, 11]
    
    base_score = 65
    
    # 1. Foundation
    h6_sign = get_sign_name((get_sign_number(asc_sign) + 6 - 1) % 12 or 12)
    h6_lord = get_lord(h6_sign)
    points.append(f"<b>Financial Burden Foundation:</b> Your debt and liability path is influenced by <b>{h6_sign}</b> energy, governed by <b>{h6_lord}</b> influences.")

    # 2. Key Significator (Mars for Debts/Enemies)
    mars_pos = planetary_pos.get('Mars', '')
    m_house = calculate_house(get_planet_sign(mars_pos), asc_sign)
    if m_house in [6, 12]:
         points.append(f"<b>Debt Significator:</b> Mars in the {get_ordinal(m_house)} house suggests a need for aggressive debt management.")

    # 3. House-by-House Impacts
    area_map = {
        6: "Debt Responsibility",
        12: "Financial Outflows"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                  nature = get_planet_nature(planet)
                  outcome = get_house_outcome(house_num, type='neg', category='Finance')
                  points.append(f"<b>{area}:</b> {planet}'s presence brings <b>{nature}</b> here, triggering <b>{outcome}</b>.")
                  found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers <b>{get_house_outcome(house_num, category='Finance', type='neg')}</b>.")

    # 4. Strategic Advice
    advice = "Ensure careful financial planning and avoid unnecessary high-interest liabilities."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses, category='Finance'))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses, category='Finance'))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses, category='Finance'))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Debts & Liabilities"))

    # Remedies Integration
    remedies = get_general_remedies("finance")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
