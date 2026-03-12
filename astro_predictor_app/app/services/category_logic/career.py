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
    
    # Target Houses for Career: 10 (Career), 6 (Service), 1 (Status)
    target_houses = [10, 6, 1]
    
    base_score = 60
    
    # 1. Foundation
    h10_sign = get_sign_name((get_sign_number(asc_sign) + 10 - 1) % 12 or 12)
    h10_lord = get_lord(h10_sign)
    points.append(f"<b>Career Foundation:</b> Your professional path is governed by **{h10_sign}** energy and **{h10_lord}** influences.")

    # 2. Key Significator (Saturn for Career/Karma)
    saturn_pos = planetary_pos.get('Saturn', '')
    s_sign = get_planet_sign(saturn_pos)
    s_house = calculate_house(s_sign, asc_sign)
    s_dignity = get_dignity('Saturn', s_sign)
    points.append(f"<b>Primary Significator:</b> Saturn (planet of work) is in the {get_ordinal(s_house)} house in **{s_sign}**.")
    points.append(f"<b>Professional Discipline:</b> Saturn triggers **{get_house_outcome(s_house, type='pos' if s_dignity != 'Debilitated' else 'neg')}** in your career life.")

    if s_dignity == 'Debilitated':
        base_score -= 10
        points.append("<b>Challenge:</b> Saturn is restricted, implying that success comes through significant discipline and hard work.")
    elif s_dignity == 'Exalted':
        base_score += 10
        points.append("<b>Strength:</b> Saturn is powerful, providing endurance and long-term career stability.")

    # 3. House-by-House Impacts
    area_map = {
        10: "Job & Status",
        6: "Daily Service",
        1: "Professional Identity"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                 nature = get_planet_nature(planet)
                 outcome = get_house_outcome(house_num, type='pos' if planet in ['Sun', 'Jupiter', 'Mercury'] else 'neg')
                 points.append(f"<b>{area}:</b> {planet}'s presence brings **{nature}** here, triggering **{outcome}**.")
                 if planet in ['Saturn', 'Mars', 'Rahu', 'Ketu']: base_score -= 10
                 found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers **{get_house_outcome(house_num)}**.")

    # 4. Strengths & Challenges Summary
    challenges = []
    stability = []
    for planet in ['Sun', 'Mars', h10_lord]:
        p_pos = planetary_pos.get(planet, '')
        p_sign = get_planet_sign(p_pos)
        dig = get_dignity(planet, p_sign)
        if dig == 'Debilitated' or calculate_house(p_sign, asc_sign) in [6, 8, 12]:
            challenges.append(planet)
        elif dig == 'Exalted' or get_lord(p_sign) == planet:
            stability.append(planet)

    if challenges:
        points.append(f"<b>Challenges:</b> **{', '.join(challenges)}** show some professional hurdles, requiring careful planning.")
    if stability:
        points.append(f"<b>Stability:</b> **{', '.join(stability)}** are well-placed, supporting consistent growth and recognition.")

    # 5. Kendra Action Potential
    kendras = [p for p, pos in planetary_pos.items() if calculate_house(get_planet_sign(pos), asc_sign) in [1, 4, 7, 10] and p != 'Mandhi']
    if kendras:
        points.append(f"<b>Active Influences:</b> **{', '.join(kendras)}** are in central houses, making them active drivers of your professional status.")

    # 6. Strategic Advice
    advice = "Maintain consistent work ethics and focus on long-term goals rather than short-term diversions."
    if base_score < 50:
        advice = "Focus on specialized skills and maintain a patient approach during workplace transitions."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Career"))

    # Remedies Integration
    remedies = get_general_remedies("career")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
