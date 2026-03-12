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
    
    # Target Houses for Legal: 6 (Litigation), 10 (Judgement/Authority), 7 (Opponents)
    target_houses = [6, 10, 7]
    
    base_score = 60
    
    # 1. Foundation
    h6_sign = get_sign_name((get_sign_number(asc_sign) + 6 - 1) % 12 or 12)
    h6_lord = get_lord(h6_sign)
    points.append(f"<b>Legal Dynamics Foundation:</b> Your legal and dispute resolution path is influenced by **{h6_sign}** energy, governed by **{h6_lord}**.")

    # 2. Key Significator (Jupiter for Law/Justice)
    jupiter_pos = planetary_pos.get('Jupiter', '')
    j_sign = get_planet_sign(jupiter_pos)
    j_house = calculate_house(j_sign, asc_sign)
    j_dignity = get_dignity('Jupiter', j_sign)
    points.append(f"<b>Justice Significator:</b> Jupiter (planet of justice) is in the {get_ordinal(j_house)} house in **{j_sign}**.")
    points.append(f"<b>Judicial Outcome:</b> Jupiter triggers **{get_house_outcome(j_house, type='pos' if j_dignity != 'Debilitated' else 'neg')}** in your legal matters.")

    if j_dignity == 'Debilitated':
        base_score -= 10
        points.append("<b>Challenge:</b> Jupiter is restricted, suggesting that legal wins require flawless documentation and patience.")
    elif j_dignity == 'Exalted':
        base_score += 10
        points.append("<b>Strength:</b> Jupiter is powerful, naturally favoring fair resolutions and judicial success.")

    # 3. House-by-House Impacts
    area_map = {
        6: "Disputes & Litigation",
        10: "Authority & Judgement",
        7: "Opponent Strength"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                 nature = get_planet_nature(planet)
                 outcome = get_house_outcome(house_num, type='pos' if planet in ['Jupiter', 'Venus', 'Mercury'] else 'neg')
                 points.append(f"<b>{area}:</b> {planet}'s presence brings **{nature}** here, triggering **{outcome}**.")
                 if planet in ['Saturn', 'Mars', 'Rahu', 'Ketu']: base_score -= 10
                 found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers **{get_house_outcome(house_num)}**.")

    # 4. Strengths & Challenges Summary
    challenges = []
    stability = []
    for planet in ['Jupiter', 'Sun', h6_lord]:
        p_pos = planetary_pos.get(planet, '')
        if not p_pos: continue
        p_sign = get_planet_sign(p_pos)
        dig = get_dignity(planet, p_sign)
        if dig == 'Debilitated' or calculate_house(p_sign, asc_sign) in [8, 12]:
            challenges.append(planet)
        elif dig == 'Exalted' or get_lord(p_sign) == planet:
            stability.append(planet)

    if challenges:
        points.append(f"<b>Challenges:</b> **{', '.join(challenges)}** show some legal hurdles, necessitating expert counsel.")
    if stability:
        points.append(f"<b>Stability:</b> **{', '.join(stability)}** are well-placed, supporting favorable legal outcomes.")

    # 5. Kendra Action Potential
    kendras = [p for p, pos in planetary_pos.items() if calculate_house(get_planet_sign(pos), asc_sign) in [1, 4, 7, 10] and p != 'Mandhi']
    if kendras:
        points.append(f"<b>Active Influences:</b> **{', '.join(kendras)}** are in central houses, actively driving your legal choices.")

    # 6. Strategic Advice
    advice = "Maintain transparent records and seek professional legal advice early in any dispute."
    if base_score < 50:
        advice = "Aim for out-of-court settlements if possible during this challenging planetary phase."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Legal Matters"))

    # Remedies Integration
    remedies = get_general_remedies("legal")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
