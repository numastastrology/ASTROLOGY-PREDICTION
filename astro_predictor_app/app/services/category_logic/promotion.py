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
    
    # Target Houses for Promotion: 10 (Career Status), 11 (Gains), 1 (Recognition)
    target_houses = [10, 11, 1]
    
    base_score = 60
    
    # 1. Foundation
    h10_sign = get_sign_name((get_sign_number(asc_sign) + 10 - 1) % 12 or 12)
    h10_lord = get_lord(h10_sign)
    points.append(f"<b>Promotion Outlook Foundation:</b> Your career advancement path is influenced by **{h10_sign}** energy, governed by **{h10_lord}**.")

    # 2. Key Significator (Sun for Authority/Recognition)
    sun_pos = planetary_pos.get('Sun', '')
    s_sign = get_planet_sign(sun_pos)
    s_house = calculate_house(s_sign, asc_sign)
    s_dignity = get_dignity('Sun', s_sign)
    points.append(f"<b>Authority Significator:</b> The Sun (planet of recognition) is in the {get_ordinal(s_house)} house in **{s_sign}**.")
    points.append(f"<b>Elevation Potential:</b> The Sun triggers **{get_house_outcome(s_house, type='pos' if s_dignity != 'Debilitated' else 'neg')}** in your professional life.")

    if s_dignity == 'Debilitated':
        base_score -= 10
        points.append("<b>Challenge:</b> The Sun is restricted, suggesting that promotion comes through proving your value to authority figures.")
    elif s_dignity == 'Exalted':
        base_score += 10
        points.append("<b>Strength:</b> The Sun is powerful, naturally attracting leadership roles and professional recognition.")

    # 3. House-by-House Impacts
    area_map = {
        10: "Career Elevation",
        11: "Income Increase",
        1: "Status Recognition"
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
        if not p_pos: continue
        p_sign = get_planet_sign(p_pos)
        dig = get_dignity(planet, p_sign)
        if dig == 'Debilitated' or calculate_house(p_sign, asc_sign) in [6, 8, 12]:
            challenges.append(planet)
        elif dig == 'Exalted' or get_lord(p_sign) == planet:
            stability.append(planet)

    if challenges:
        points.append(f"<b>Challenges:</b> **{', '.join(challenges)}** show some hurdles in advancement, requiring extra dedication.")
    if stability:
        points.append(f"<b>Stability:</b> **{', '.join(stability)}** are well-placed, supporting steady and favorable professional growth.")

    # 5. Kendra Action Potential
    kendras = [p for p, pos in planetary_pos.items() if calculate_house(get_planet_sign(pos), asc_sign) in [1, 4, 7, 10] and p != 'Mandhi']
    if kendras:
        points.append(f"<b>Active Influences:</b> **{', '.join(kendras)}** are in central houses, actively driving your professional elevation.")

    # 6. Strategic Advice
    advice = "Continue to showcase leadership skills and take on additional responsibilities proactively."
    if base_score < 50:
        advice = "Wait for a more favorable planetary alignment before seeking a major role elevation."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Promotion"))

    # Remedies Integration
    remedies = get_general_remedies("career")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
