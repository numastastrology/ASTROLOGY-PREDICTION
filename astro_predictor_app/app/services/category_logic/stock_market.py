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
    
    # Target Houses for Stock: 5 (Speculation), 11 (Gains), 2 (Wealth), 9 (Fortune)
    target_houses = [5, 11, 2, 9]
    
    base_score = 60
    
    # 1. Foundation
    h5_sign = get_sign_name((get_sign_number(asc_sign) + 5 - 1) % 12 or 12)
    h5_lord = get_lord(h5_sign)
    points.append(f"<b>Speculative Foundation:</b> Your stock market and speculation path is influenced by **{h5_sign}** energy, governed by **{h5_lord}**.")

    # 2. Key Significator (Mercury for Calculation/Rahu for sudden gains)
    mercury_pos = planetary_pos.get('Mercury', '')
    m_sign = get_planet_sign(mercury_pos)
    m_house = calculate_house(m_sign, asc_sign)
    m_dignity = get_dignity('Mercury', m_sign)
    points.append(f"<b>Primary Significator:</b> Mercury (planet of calculation) is in the {get_ordinal(m_house)} house in **{m_sign}**.")
    points.append(f"<b>Analytical Instinct:</b> Mercury triggers **{get_house_outcome(m_house, type='pos' if m_dignity != 'Debilitated' else 'neg')}** in your speculative decisions.")

    if m_dignity == 'Debilitated':
        base_score -= 10
        points.append("<b>Challenge:</b> Mercury is restricted, suggesting that impulsive decisions might lead to speculative hurdles.")
    elif m_dignity == 'Exalted':
        base_score += 10
        points.append("<b>Strength:</b> Mercury is powerful, providing sharp market timing and calculative success.")

    # 3. House-by-House Impacts
    area_map = {
        5: "Speculative Wisdom",
        11: "Market Gains",
        2: "Wealth Accumulation",
        9: "Investment Luck"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                 nature = get_planet_nature(planet)
                 outcome = get_house_outcome(house_num, type='pos' if planet in ['Jupiter', 'Venus', 'Mercury', 'Rahu'] else 'neg')
                 points.append(f"<b>{area}:</b> {planet}'s presence brings **{nature}** here, triggering **{outcome}**.")
                 if planet in ['Saturn', 'Mars', 'Ketu']: base_score -= 10
                 found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers **{get_house_outcome(house_num)}**.")

    # 4. Strengths & Challenges Summary
    challenges = []
    stability = []
    for planet in ['Mercury', 'Jupiter', h5_lord]:
        p_pos = planetary_pos.get(planet, '')
        if not p_pos: continue
        p_sign = get_planet_sign(p_pos)
        dig = get_dignity(planet, p_sign)
        if dig == 'Debilitated' or calculate_house(p_sign, asc_sign) in [6, 8, 12]:
            challenges.append(planet)
        elif dig == 'Exalted' or get_lord(p_sign) == planet:
            stability.append(planet)

    if challenges:
        points.append(f"<b>Challenges:</b> **{', '.join(challenges)}** show some speculative hurdles, requiring cautious timing.")
    if stability:
        points.append(f"<b>Stability:</b> **{', '.join(stability)}** are well-placed, supporting steady and favorable investment growth.")

    # 5. Kendra Action Potential
    kendras = [p for p, pos in planetary_pos.items() if calculate_house(get_planet_sign(pos), asc_sign) in [1, 4, 7, 10] and p != 'Mandhi']
    if kendras:
        points.append(f"<b>Active Influences:</b> **{', '.join(kendras)}** are in central houses, actively driving your market choices.")

    # 6. Strategic Advice
    advice = "Maintain a long-term investment perspective and avoid emotional market decisions."
    if base_score < 50:
        advice = "Exercise extreme caution in speculation and wait for more stable planetary configurations."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Stock Market"))

    # Remedies Integration
    remedies = get_general_remedies("stock_market")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
