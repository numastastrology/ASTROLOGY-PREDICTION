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
    
    # Target Houses for Children: 5 (Primary), 9 (Fortune), 11 (Gains)
    target_houses = [5, 9, 11]
    
    base_score = 60
    
    # 1. Foundation
    h5_sign = get_sign_name((get_sign_number(asc_sign) + 5 - 1) % 12 or 12)
    h5_lord = get_lord(h5_sign)
    points.append(f"<b>Progeny Foundation:</b> Your path regarding children is influenced by **{h5_sign}** energy, governed by **{h5_lord}**.")

    # 2. Key Significator (Jupiter)
    jupiter_pos = planetary_pos.get('Jupiter', '')
    j_sign = get_planet_sign(jupiter_pos)
    j_house = calculate_house(j_sign, asc_sign)
    j_dignity = get_dignity('Jupiter', j_sign)
    points.append(f"<b>Primary Significator:</b> Jupiter (planet of progeny) is in the {get_ordinal(j_house)} house in **{j_sign}**.")
    points.append(f"<b>Happiness through Children:</b> Jupiter triggers **{get_house_outcome(j_house, type='pos' if j_dignity != 'Debilitated' else 'neg')}** in your life.")

    if j_dignity == 'Debilitated':
        base_score -= 10
        points.append("<b>Challenge:</b> Jupiter is restricted here, requiring more conscious care regarding children's matters.")
    elif j_dignity == 'Exalted':
        base_score += 10
        points.append("<b>Strength:</b> Jupiter is powerful, enhancing joy and success through children.")

    # 3. House-by-House Impacts
    area_map = {
        5: "Intelligence & Progeny",
        9: "Fortunate Outcomes",
        11: "Fulfillment of Desires"
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
    for planet in ['Jupiter', 'Moon', h5_lord]:
        p_pos = planetary_pos.get(planet, '')
        p_sign = get_planet_sign(p_pos)
        dig = get_dignity(planet, p_sign)
        if dig == 'Debilitated' or calculate_house(p_sign, asc_sign) in [6, 8, 12]:
            challenges.append(planet)
        elif dig == 'Exalted' or get_lord(p_sign) == planet:
            stability.append(planet)

    if challenges:
        points.append(f"<b>Challenges:</b> **{', '.join(challenges)}** show some restrictions, suggesting a need for patience and guidance.")
    if stability:
        points.append(f"<b>Stability:</b> **{', '.join(stability)}** are well-placed, providing a protective and favorable influence for progeny.")

    # 5. Kendra Action Potential
    kendras = [p for p, pos in planetary_pos.items() if calculate_house(get_planet_sign(pos), asc_sign) in [1, 4, 7, 10] and p != 'Mandhi']
    if kendras:
        points.append(f"<b>Active Influences:</b> **{', '.join(kendras)}** are in central houses, actively shaping the creative and emotional aspects of family life.")

    # 6. Strategic Advice
    advice = "Focus on nurturing the unique talents of children and provide a stable, supportive environment for their growth."
    if base_score < 50:
        advice = "Spend quality time daily and stay patient during intellectual or creative developmental shifts."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Children"))

    # Remedies Integration
    remedies = get_general_remedies("children")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
