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
    
    # Target Houses for Health: 6 (Illness), 8 (Protection), 1 (Vitality)
    target_houses = [6, 8, 1]
    
    base_score = 60
    
    # 1. Foundation
    h1_sign = asc_sign
    h1_lord = get_lord(h1_sign)
    points.append(f"<b>Vitality Foundation:</b> Your physical strength is governed by **{h1_sign}** energy, led by **{h1_lord}**.")

    # 2. Key Significator (Sun for Vitality)
    sun_pos = planetary_pos.get('Sun', '')
    s_sign = get_planet_sign(sun_pos)
    s_house = calculate_house(s_sign, asc_sign)
    s_dignity = get_dignity('Sun', s_sign)
    points.append(f"<b>Vitality Significator:</b> The Sun (planet of health) is in the {get_ordinal(s_house)} house in **{s_sign}**.")
    points.append(f"<b>Physical Energy:</b> The Sun triggers **{get_house_outcome(s_house, type='pos' if s_dignity != 'Debilitated' else 'neg')}**.")

    if s_dignity == 'Debilitated':
        base_score -= 10
        points.append("<b>Challenge:</b> Sun's low strength suggests a need for consistent focus on diet and energy management.")
    elif s_dignity == 'Exalted':
        base_score += 10
        points.append("<b>Strength:</b> Strong Sun provides high immunity and a resilient physical constitution.")

    # 3. House-by-House Impacts
    area_map = {
        6: "Physical Well-being",
        8: "Life Protection",
        1: "Self-Vitality"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                 nature = get_planet_nature(planet)
                 outcome = get_house_outcome(house_num, type='pos' if planet in ['Jupiter', 'Venus', 'Moon'] else 'neg')
                 points.append(f"<b>{area}:</b> {planet}'s presence brings **{nature}** here, triggering **{outcome}**.")
                 if planet in ['Saturn', 'Mars', 'Rahu', 'Ketu']: base_score -= 10
                 found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers **{get_house_outcome(house_num)}**.")

    # 4. Strengths & Challenges Summary
    challenges = []
    stability = []
    for planet in ['Sun', 'Mars', h1_lord]:
        p_pos = planetary_pos.get(planet, '')
        p_sign = get_planet_sign(p_pos)
        dig = get_dignity(planet, p_sign)
        if dig == 'Debilitated' or calculate_house(p_sign, asc_sign) in [6, 8, 12]:
            challenges.append(planet)
        elif dig == 'Exalted' or get_lord(p_sign) == planet:
            stability.append(planet)

    if challenges:
        points.append(f"<b>Challenges:</b> **{', '.join(challenges)}** show some physical hurdles, requiring careful health management.")
    if stability:
        points.append(f"<b>Stability:</b> **{', '.join(stability)}** are well-placed, supporting long-term health and vitality.")

    # 5. Kendra Action Potential
    kendras = [p for p, pos in planetary_pos.items() if calculate_house(get_planet_sign(pos), asc_sign) in [1, 4, 7, 10] and p != 'Mandhi']
    if kendras:
        points.append(f"<b>Active Influences:</b> **{', '.join(kendras)}** are in central houses, actively impacting your health routines.")

    # 6. Strategic Advice
    advice = "Maintain a steady daily routine and prioritize physical activities that boost immunity."
    if base_score < 50:
        advice = "Monitor physical energy levels closely and avoid over-exertion during this cycle."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Health"))

    # Remedies Integration
    remedies = get_general_remedies("health")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
