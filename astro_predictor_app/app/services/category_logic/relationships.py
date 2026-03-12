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
    
    # Target Houses for Relationships: 7 (Spouse), 2 (Family), 4 (Domestic), 8 (In-laws), 12 (Bed Pleasures)
    target_houses = [7, 2, 4, 8, 12]
    
    base_score = 60
    
    # 1. Foundation
    h7_sign = get_sign_name((get_sign_number(asc_sign) + 7 - 1) % 12 or 12)
    h7_lord = get_lord(h7_sign)
    points.append(f"<b>Relationship Foundation:</b> Your marital path is influenced by **{h7_sign}** energy, governed by **{h7_lord}**.")

    # 2. Key Significator (Venus)
    venus_pos = planetary_pos.get('Venus', '')
    v_sign = get_planet_sign(venus_pos)
    v_house = calculate_house(v_sign, asc_sign)
    v_dignity = get_dignity('Venus', v_sign)
    points.append(f"<b>Primary Significator:</b> Venus (planet of love) is in the {get_ordinal(v_house)} house in **{v_sign}**.")
    points.append(f"<b>Romantic Style:</b> Venus triggers **{get_house_outcome(v_house, type='pos' if v_dignity != 'Debilitated' else 'neg')}** in your personal life.")

    if v_dignity == 'Debilitated':
        base_score -= 10
        points.append("<b>Challenge:</b> Venus is restricted here, requiring more conscious effort in understanding partner needs.")
    elif v_dignity == 'Exalted':
        base_score += 10
        points.append("<b>Strength:</b> Venus is powerful, enhancing charm and relationship stability.")

    # 3. House-by-House Impacts
    area_map = {
        7: "Partnership Focus",
        2: "Family Harmony",
        4: "Domestic Peace",
        8: "In-law Relations",
        12: "Inner Connection"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                 nature = get_planet_nature(planet)
                 outcome = get_house_outcome(house_num, type='pos' if planet in ['Jupiter', 'Venus', 'Mercury', 'Moon'] else 'neg')
                 points.append(f"<b>{area}:</b> {planet}'s presence brings **{nature}** here, triggering **{outcome}**.")
                 if planet in ['Saturn', 'Mars', 'Rahu', 'Ketu']: base_score -= 10
                 found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers **{get_house_outcome(house_num)}**.")

    # 4. Strengths & Challenges Summary
    challenges = []
    stability = []
    for planet in ['Venus', 'Jupiter', h7_lord]:
        p_pos = planetary_pos.get(planet, '')
        p_sign = get_planet_sign(p_pos)
        dig = get_dignity(planet, p_sign)
        if dig == 'Debilitated' or calculate_house(p_sign, asc_sign) in [6, 8, 12]:
            challenges.append(planet)
        elif dig == 'Exalted' or get_lord(p_sign) == planet:
            stability.append(planet)

    if challenges:
        points.append(f"<b>Challenges:</b> **{', '.join(challenges)}** show some restrictions, reminding you to handle sensitive issues with care.")
    if stability:
        points.append(f"<b>Stability:</b> **{', '.join(stability)}** are well-placed, providing a strong anchor for long-term bonds.")

    # 5. Kendra Action Potential
    kendras = [p for p, pos in planetary_pos.items() if calculate_house(get_planet_sign(pos), asc_sign) in [1, 4, 7, 10] and p != 'Mandhi']
    if kendras:
        points.append(f"<b>Active Influences:</b> **{', '.join(kendras)}** are in key pivot houses, making them active drivers of your relationship status.")

    # 6. Strategic Advice
    advice = "Maintain open communication and prioritize shared long-term goals over temporary disagreements."
    if base_score < 50:
        advice = "Cultivate extra patience and seek mutual understanding specifically in areas of domestic disagreement."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic (Aspects/Transits/Dasa)
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Relationships"))

    # Remedies Integration
    remedies = get_general_remedies("relationships")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
