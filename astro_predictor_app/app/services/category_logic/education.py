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
    
    # Target Houses for Education: 4 (Primary), 5 (Intelligence), 9 (Higher Studies)
    target_houses = [4, 5, 9]
    
    base_score = 60
    
    # 1. Foundation
    h4_sign = get_sign_name((get_sign_number(asc_sign) + 4 - 1) % 12 or 12)
    h4_lord = get_lord(h4_sign)
    points.append(f"<b>Academic Foundation:</b> Your educational path is influenced by **{h4_sign}** energy, governed by **{h4_lord}**.")

    # 2. Key Significator (Mercury for Intellect/Education)
    mercury_pos = planetary_pos.get('Mercury', '')
    m_sign = get_planet_sign(mercury_pos)
    m_house = calculate_house(m_sign, asc_sign)
    m_dignity = get_dignity('Mercury', m_sign)
    points.append(f"<b>Primary Significator:</b> Mercury (planet of intellect) is in the {get_ordinal(m_house)} house in **{m_sign}**.")
    points.append(f"<b>Learning Style:</b> Mercury triggers **{get_house_outcome(m_house, type='pos' if m_dignity != 'Debilitated' else 'neg')}** in your academic pursuits.")

    if m_dignity == 'Debilitated':
        base_score -= 10
        points.append("<b>Challenge:</b> Mercury is restricted, suggesting that focus and methodical study are key to overcoming hurdles.")
    elif m_dignity == 'Exalted':
        base_score += 10
        points.append("<b>Strength:</b> Mercury is powerful, providing sharp analytical skills and academic success.")

    # 3. House-by-House Impacts
    area_map = {
        4: "Primary Knowledge",
        5: "Specialized Intelligence",
        9: "Higher Learning"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                 nature = get_planet_nature(planet)
                 outcome = get_house_outcome(house_num, type='pos' if planet in ['Jupiter', 'Mercury', 'Venus'] else 'neg')
                 points.append(f"<b>{area}:</b> {planet}'s presence brings **{nature}** here, triggering **{outcome}**.")
                 if planet in ['Saturn', 'Mars', 'Rahu', 'Ketu']: base_score -= 10
                 found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers **{get_house_outcome(house_num)}**.")

    # 4. Strengths & Challenges Summary
    challenges = []
    stability = []
    for planet in ['Mercury', 'Jupiter', h4_lord]:
        p_pos = planetary_pos.get(planet, '')
        p_sign = get_planet_sign(p_pos)
        dig = get_dignity(planet, p_sign)
        if dig == 'Debilitated' or calculate_house(p_sign, asc_sign) in [6, 8, 12]:
            challenges.append(planet)
        elif dig == 'Exalted' or get_lord(p_sign) == planet:
            stability.append(planet)

    if challenges:
        points.append(f"<b>Challenges:</b> **{', '.join(challenges)}** show some academic restrictions, requiring consistent concentration.")
    if stability:
        points.append(f"<b>Stability:</b> **{', '.join(stability)}** are well-placed, supporting steady educational milestones.")

    # 5. Kendra Action Potential
    kendras = [p for p, pos in planetary_pos.items() if calculate_house(get_planet_sign(pos), asc_sign) in [1, 4, 7, 10] and p != 'Mandhi']
    if kendras:
        points.append(f"<b>Active Influences:</b> **{', '.join(kendras)}** are in central houses, actively driving your educational decisions.")

    # 6. Strategic Advice
    advice = "Maintain a disciplined study schedule and focus on foundational concepts before moving to advanced topics."
    if base_score < 50:
        advice = "Seek guidance from mentors and avoid distractions during crucial examination periods."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Education"))

    # Remedies Integration
    remedies = get_general_remedies("education")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
