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
    
    # Target Houses for Luck: 9 (Fortune), 11 (Gains), 5 (Divine Grace/Purvapunya)
    target_houses = [9, 11, 5]
    
    base_score = 60
    
    # 1. Foundation
    h9_sign = get_sign_name((get_sign_number(asc_sign) + 9 - 1) % 12 or 12)
    h9_lord = get_lord(h9_sign)
    points.append(f"<b>Fortune Foundation:</b> Your natural luck quotient is influenced by <b>{h9_sign}</b> energy, governed by <b>{h9_lord}</b>.")

    # 2. Key Significator (Jupiter for Fortune)
    jupiter_pos = planetary_pos.get('Jupiter', '')
    j_sign = get_planet_sign(jupiter_pos)
    j_house = calculate_house(j_sign, asc_sign)
    j_dignity = get_dignity('Jupiter', j_sign)
    points.append(f"<b>Luck Significator:</b> Jupiter (planet of fortune) is in the {get_ordinal(j_house)} house in <b>{j_sign}</b>.")
    points.append(f"<b>Opportunity Flow:</b> Jupiter triggers <b>{get_house_outcome(j_house, type='pos' if j_dignity != 'Debilitated' else 'neg')}</b> in your path.")

    if j_dignity == 'Debilitated':
        base_score -= 10
        points.append("<b>Challenge:</b> Jupiter is restricted, implying that 'luck' comes through conscious effort and merit.")
    elif j_dignity == 'Exalted':
        base_score += 10
        points.append("<b>Strength:</b> Jupiter is powerful, naturally attracting lucky breaks and divine protection.")

    # 3. House-by-House Impacts
    area_map = {
        9: "Manifest Fortune",
        11: "Ease of Gains",
        5: "Divine Protection"
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
                 points.append(f"<b>{area}:</b> {planet}'s presence brings <b>{nature}</b> here, triggering <b>{outcome}</b>.")
                 if planet in ['Saturn', 'Mars', 'Rahu', 'Ketu']: base_score -= 10
                 found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers <b>{get_house_outcome(house_num)}</b>.")

    # 4. Strengths & Challenges Summary
    challenges = []
    stability = []
    for planet in ['Jupiter', 'Venus', h9_lord]:
        p_pos = planetary_pos.get(planet, '')
        if not p_pos: continue
        p_sign = get_planet_sign(p_pos)
        dig = get_dignity(planet, p_sign)
        if dig == 'Debilitated' or calculate_house(p_sign, asc_sign) in [6, 8, 12]:
            challenges.append(planet)
        elif dig == 'Exalted' or get_lord(p_sign) == planet:
            stability.append(planet)

    if challenges:
        points.append(f"<b>Challenges:</b> <b>{', '.join(challenges)}</b> show some fortune hurdles, requiring patience in transitions.")
    if stability:
        points.append(f"<b>Stability:</b> <b>{', '.join(stability)}</b> are well-placed, providing a protective and favorable luck factor.")

    # 5. Kendra Action Potential
    kendras = [p for p, pos in planetary_pos.items() if calculate_house(get_planet_sign(pos), asc_sign) in [1, 4, 7, 10] and p != 'Mandhi']
    if kendras:
        points.append(f"<b>Active Influences:</b> <b>{', '.join(kendras)}</b> are in central houses, actively driving your fortunate moments.")

    # 6. Strategic Advice
    advice = "Stay optimistic and recognize opportunities early to make the most of your natural fortune."
    if base_score < 50:
        advice = "Rely on merit and hard work; don't depend on 'luck' during this planetary phase."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Luck Factor"))

    # Remedies Integration
    remedies = get_general_remedies("spirituality")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
