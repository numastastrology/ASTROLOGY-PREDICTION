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
    
    # Target Houses for Job Change: 10 (Career), 6 (Service), 3 (Change/Short travel)
    target_houses = [10, 6, 3]
    
    base_score = 60
    
    # 1. Foundation
    h10_sign = get_sign_name((get_sign_number(asc_sign) + 10 - 1) % 12 or 12)
    h10_lord = get_lord(h10_sign)
    points.append(f"<b>Professional Change Foundation:</b> Your job change path is influenced by <b>{h10_sign}</b> energy, governed by <b>{h10_lord}</b>.")

    # 2. Key Significator (Saturn for Job/Persistence)
    saturn_pos = planetary_pos.get('Saturn', '')
    s_sign = get_planet_sign(saturn_pos)
    s_house = calculate_house(s_sign, asc_sign)
    s_dignity = get_dignity('Saturn', s_sign)
    points.append(f"<b>Primary Significator:</b> Saturn (planet of persistence) is in the {get_ordinal(s_house)} house in <b>{s_sign}</b>.")
    points.append(f"<b>Workplace Flux:</b> Saturn triggers <b>{get_house_outcome(s_house, type='pos' if s_dignity != 'Debilitated' else 'neg')}</b> in your career trajectory.")

    if s_dignity == 'Debilitated':
        base_score -= 10
        points.append("<b>Challenge:</b> Saturn is restricted, implying that changes might require more significant effort to secure.")
    elif s_dignity == 'Exalted':
        base_score += 10
        points.append("<b>Strength:</b> Saturn is powerful, supporting stable and favorable career transitions.")

    # 3. House-by-House Impacts
    area_map = {
        10: "Job Scope",
        6: "Daily Work Flow",
        3: "Short Transitions"
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
                 points.append(f"<b>{area}:</b> {planet}'s presence brings <b>{nature}</b> here, triggering <b>{outcome}</b>.")
                 if planet in ['Saturn', 'Mars', 'Rahu', 'Ketu']: base_score -= 10
                 found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers <b>{get_house_outcome(house_num)}</b>.")

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
        points.append(f"<b>Challenges:</b> <b>{', '.join(challenges)}</b> show some hurdles in transition, requiring patience.")
    if stability:
        points.append(f"<b>Stability:</b> <b>{', '.join(stability)}</b> are well-placed, providing a favorable influence during shifts.")

    # 5. Kendra Action Potential
    kendras = [p for p, pos in planetary_pos.items() if calculate_house(get_planet_sign(pos), asc_sign) in [1, 4, 7, 10] and p != 'Mandhi']
    if kendras:
        points.append(f"<b>Active Influences:</b> <b>{', '.join(kendras)}</b> are in central houses, actively driving your professional transitions.")

    # 6. Strategic Advice
    advice = "Thoroughly research new opportunities and ensure current commitments are met before transitioning."
    if base_score < 50:
        advice = "Exercise caution during job changes and wait for more stable planetary configurations."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Job Change"))

    # Remedies Integration
    remedies = get_general_remedies("career")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
