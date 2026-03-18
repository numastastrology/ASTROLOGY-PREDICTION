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
    
    # Target Houses for Business: 7 (Partners), 10 (Career), 11 (Gains)
    target_houses = [7, 10, 11]
    
    base_score = 60
    
    # 1. Foundation
    h7_sign = get_sign_name((get_sign_number(asc_sign) + 7 - 1) % 12 or 12)
    h7_lord = get_lord(h7_sign)
    points.append(f"<b>Business Foundation:</b> Your entrepreneurial path is influenced by <b>{h7_sign}</b> energy, governed by <b>{h7_lord}</b>.")

    # 2. Key Significator (Mercury for Trade/Commerce)
    mercury_pos = planetary_pos.get('Mercury', '')
    m_sign = get_planet_sign(mercury_pos)
    m_house = calculate_house(m_sign, asc_sign)
    m_dignity = get_dignity('Mercury', m_sign)
    points.append(f"<b>Primary Significator:</b> Mercury (planet of trade) is in the {get_ordinal(m_house)} house in <b>{m_sign}</b>.")
    points.append(f"<b>Commercial Instinct:</b> Mercury triggers <b>{get_house_outcome(m_house, type='pos' if m_dignity != 'Debilitated' else 'neg')}</b> in your business ventures.")

    if m_dignity == 'Debilitated':
        base_score -= 10
        points.append("<b>Challenge:</b> Mercury is restricted, suggesting that market research and precise planning are vital.")
    elif m_dignity == 'Exalted':
        base_score += 10
        points.append("<b>Strength:</b> Mercury is powerful, providing excellent trading skills and business acumen.")

    # 3. House-by-House Impacts
    area_map = {
        7: "Partnerships & Sales",
        10: "Career Status",
        11: "Profit Gains"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                 nature = get_planet_nature(planet)
                 outcome = get_house_outcome(house_num, type='pos' if planet in ['Sun', 'Mercury', 'Jupiter'] else 'neg')
                 points.append(f"<b>{area}:</b> {planet}'s presence brings <b>{nature}</b> here, triggering <b>{outcome}</b>.")
                 if planet in ['Saturn', 'Mars', 'Rahu', 'Ketu']: base_score -= 10
                 found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers <b>{get_house_outcome(house_num)}</b>.")

    # 4. Strengths & Challenges Summary
    challenges = []
    stability = []
    for planet in ['Mercury', 'Sun', h7_lord]:
        p_pos = planetary_pos.get(planet, '')
        if not p_pos: continue
        p_sign = get_planet_sign(p_pos)
        dig = get_dignity(planet, p_sign)
        if dig == 'Debilitated' or calculate_house(p_sign, asc_sign) in [6, 8, 12]:
            challenges.append(planet)
        elif dig == 'Exalted' or get_lord(p_sign) == planet:
            stability.append(planet)

    if challenges:
        points.append(f"<b>Challenges:</b> <b>{', '.join(challenges)}</b> show some market hurdles, requiring cautious investment.")
    if stability:
        points.append(f"<b>Stability:</b> <b>{', '.join(stability)}</b> are well-placed, supporting steady growth and commercial success.")

    # 5. Kendra Action Potential
    kendras = [p for p, pos in planetary_pos.items() if calculate_house(get_planet_sign(pos), asc_sign) in [1, 4, 7, 10] and p != 'Mandhi']
    if kendras:
        points.append(f"<b>Active Influences:</b> <b>{', '.join(kendras)}</b> are in key pivot houses, making them active drivers of your business status.")

    # 6. Strategic Advice
    advice = "Focus on market networking and maintain transparent communication with partners."
    if base_score < 50:
        advice = "Avoid major business changes or starts during unfavorable Dasa sub-periods."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Business"))

    # Remedies Integration
    remedies = get_general_remedies("business")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
