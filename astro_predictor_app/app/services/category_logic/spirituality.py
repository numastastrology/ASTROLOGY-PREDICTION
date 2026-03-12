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
    
    # Target Houses for Spirituality: 12 (Liberation), 8 (Deep secrets), 9 (Wisdom/Faith)
    target_houses = [12, 8, 9]
    
    base_score = 60
    
    # 1. Foundation
    h12_sign = get_sign_name((get_sign_number(asc_sign) + 12 - 1) % 12 or 12)
    h12_lord = get_lord(h12_sign)
    points.append(f"<b>Spiritual Path Foundation:</b> Your inner growth and spiritual path is influenced by **{h12_sign}** energy, governed by **{h12_lord}**.")

    # 2. Key Significator (Ketu for Liberation/Jupiter for Wisdom)
    ketu_pos = planetary_pos.get('Ketu', '')
    k_sign = get_planet_sign(ketu_pos)
    k_house = calculate_house(k_sign, asc_sign)
    points.append(f"<b>Primary Significator:</b> Ketu (planet of detachment) is in the {get_ordinal(k_house)} house in **{k_sign}**.")
    points.append(f"<b>Inner Awakening:</b> Ketu triggers **{get_house_outcome(k_house, type='pos' if k_house in [8, 12] else 'neg')}** in your spiritual journey.")

    # 3. House-by-House Impacts
    area_map = {
        12: "Inner Liberation",
        8: "Mystical Insight",
        9: "Divine Wisdom"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                 nature = get_planet_nature(planet)
                 outcome = get_house_outcome(house_num, type='pos' if planet in ['Jupiter', 'Ketu', 'Sun'] else 'neg')
                 points.append(f"<b>{area}:</b> {planet}'s presence brings **{nature}** here, triggering **{outcome}**.")
                 found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers **{get_house_outcome(house_num)}**.")

    # 4. Strengths & Challenges Summary
    challenges = []
    stability = []
    for planet in ['Jupiter', 'Ketu', h12_lord]:
        p_pos = planetary_pos.get(planet, '')
        if not p_pos: continue
        p_sign = get_planet_sign(p_pos)
        dig = get_dignity(planet, p_sign)
        if calculate_house(p_sign, asc_sign) not in [8, 9, 12]:
            challenges.append(planet)
        else:
            stability.append(planet)

    if challenges:
        points.append(f"<b>Challenges:</b> **{', '.join(challenges)}** show some hurdles in inner peace, requiring dedicated practice.")
    if stability:
        points.append(f"<b>Stability:</b> **{', '.join(stability)}** are well-placed, providing a favorable influence for mystical growth.")

    # 5. Kendra Action Potential
    kendras = [p for p, pos in planetary_pos.items() if calculate_house(get_planet_sign(pos), asc_sign) in [1, 4, 7, 10] and p != 'Mandhi']
    if kendras:
        points.append(f"<b>Active Influences:</b> **{', '.join(kendras)}** are in central houses, actively driving your spiritual choices.")

    # 6. Strategic Advice
    advice = "Dedicate time daily for meditation and focus on inner detachment from material concerns."
    if base_score < 50:
        advice = "Focus on basics and maintain steady faith during this transformational planetary period."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Spirituality"))

    # Remedies Integration
    remedies = get_general_remedies("spirituality")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
