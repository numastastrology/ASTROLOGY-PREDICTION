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
    
    # Target Houses for Career Comparison: 7 (Business), 10 (Career/Job), 6 (Service)
    target_houses = [7, 10, 6]
    
    base_score = 60
    
    # 1. Foundation Comparison
    h7_sign = get_sign_name((get_sign_number(asc_sign) + 7 - 1) % 12 or 12)
    h7_lord = get_lord(h7_sign)
    h10_sign = get_sign_name((get_sign_number(asc_sign) + 10 - 1) % 12 or 12)
    h10_lord = get_lord(h10_sign)
    
    points.append(f"<b>Business Foundation:</b> Entrepreneurial path governed by <b>{h7_sign}</b> and <b>{h7_lord}</b> influences.")
    points.append(f"<b>Job Foundation:</b> Service path governed by <b>{h10_sign}</b> and <b>{h10_lord}</b> influences.")

    # 2. Key Significators (Mercury for Business / Saturn for Job)
    mercury_pos = planetary_pos.get('Mercury', '')
    m_sign = get_planet_sign(mercury_pos)
    m_dignity = get_dignity('Mercury', m_sign)
    
    saturn_pos = planetary_pos.get('Saturn', '')
    s_sign = get_planet_sign(saturn_pos)
    s_dignity = get_dignity('Saturn', s_sign)

    if m_dignity in ['Exalted', 'Normal'] and s_dignity == 'Debilitated':
        points.append("<b>Entrepreneurial Spark:</b> Strong Mercury triggers effective trade and logic, favoring <b>Business</b>.")
        base_score += 15
    elif s_dignity in ['Exalted', 'Normal'] and m_dignity == 'Debilitated':
        points.append("<b>Structural Integrity:</b> Saturn's influence provides the discipline needed for long-term <b>Service (Job)</b> careers.")
        base_score -= 15
    else:
        points.append("<b>Balanced Potency:</b> Indicators for both paths are present, suggesting flexibility.")

    # 3. House-by-House Impacts
    area_map = {
        7: "Partnership Potential",
        10: "Authority Status",
        6: "Service Consistency"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                  nature = get_planet_nature(planet)
                  outcome = get_house_outcome(house_num, type='pos' if planet in ['Sun', 'Jupiter', 'Mercury', 'Venus'] else 'neg', category='Career')
                  points.append(f"<b>{area}:</b> {planet}'s presence brings <b>{nature}</b> here, triggering <b>{outcome}</b>.")
                  found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers <b>{get_house_outcome(house_num, category='Career')}</b>.")

    # 4. Kendra Action Potential
    kendras = [p for p, pos in planetary_pos.items() if calculate_house(get_planet_sign(pos), asc_sign) in [1, 4, 7, 10] and p != 'Mandhi']
    if kendras:
        points.append(f"<b>Active Influences:</b> <b>{', '.join(kendras)}</b> are in key pivot houses, driving your career choice status.")

    # 5. Final Strategic Recommendation
    if base_score > 65:
        recommendation = "A path in <b>Business or Independent Trade</b> is highly favorable based on current planetary strengths."
    elif base_score < 55:
        recommendation = "A stable <b>Job or Service-oriented Career</b> is favored for long-term growth and security."
    else:
        recommendation = "A <b>Balanced Profile</b>; success is possible in both Job and Business depending on the current period."
    
    # --- Dynamic Business Synthesis ---
    from astro_predictor_app.app.utils.astro_utils import get_dynamic_recommendations
    dynamic_insights = get_dynamic_recommendations(planetary_pos, asc_sign, 'Business')

    points.append("<b>Top Recommended Business Paths:</b>")
    
    lagna_recs = []
    # Combine and limit
    combined_recs = dynamic_insights + lagna_recs
    final_recs = []
    seen = set()
    for r in combined_recs:
        if r and r not in seen:
            final_recs.append(r)
            seen.add(r)
            if len(final_recs) >= 5: break

    for rec in final_recs:
        points.append(f"• {rec}")

    points.append(f"<b>Strategic Recommendation:</b> {recommendation}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses, category='Career'))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses, category='Career'))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses, category='Career'))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Career Comparison"))

    # Remedies Integration
    remedies = get_general_remedies("business")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "recommendation": recommendation,
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
