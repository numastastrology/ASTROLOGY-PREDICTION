from astro_predictor_app.app.utils.astro_utils import (
    get_sign_number, get_sign_name, get_planet_sign, calculate_house, get_lord,
    get_planet_nature, get_house_outcome, get_ordinal, get_dignity, get_nak_info,
    analyze_planetary_combinations, analyze_planetary_aspects, analyze_transits, analyze_jamakkol, analyze_dasa_bhukti_detailed
)
from astro_predictor_app.app.utils.remedy_utils import get_general_remedies, get_dasa_remedies
from astro_predictor_app.app.utils.description_utils import LAGNA_HOUSE_INDICATORS, PADA_TRAITS

def analyze(birth_details, chart_data, dasa_info=None):
    points = []
    asc_sign = chart_data.get('ascendant', '')
    planetary_pos = chart_data.get('planetary_positions', {})
    transit_pos = chart_data.get('transit_positions', {})
    jamakkol_data = chart_data.get('jamakkol', {})
    
    # Get Nakshatra/Pada for Moon
    moon_pos = planetary_pos.get('Moon', '')
    nak_info = get_nak_info(moon_pos)
    nakshatra = nak_info['name'] if nak_info else 'Unknown'
    pada = str(nak_info['pada']) if nak_info else 'Unknown'
    
    # Target Houses for Education: 4 (Early), 2 (Academic), 5 (Intelligence), 9 (Higher)
    target_houses = [4, 2, 5, 9]
    
    base_score = 65
    
    # 1. Foundation
    h4_sign = get_sign_name((get_sign_number(asc_sign) + 4 - 1) % 12 or 12)
    h4_lord = get_lord(h4_sign)
    points.append(f"<b>Educational Foundation:</b> Your learning path is influenced by <b>{h4_sign}</b> energy, governed by <b>{h4_lord}</b> influences.")

    if asc_sign in LAGNA_HOUSE_INDICATORS:
        indicators = LAGNA_HOUSE_INDICATORS[asc_sign].get("Education", [])
        points.extend(indicators)

    # 2. Key Significator (Mercury for Intellect)
    mercury_pos = planetary_pos.get('Mercury', '')
    m_sign = get_planet_sign(mercury_pos)
    m_house = calculate_house(m_sign, asc_sign)
    m_dignity = get_dignity('Mercury', m_sign)
    points.append(f"<b>Intellectual Significator:</b> Mercury is in the {get_ordinal(m_house)} house in <b>{m_sign}</b>.")
    points.append(f"<b>Cognitive Ability:</b> Mercury triggers <b>{get_house_outcome(m_house, type='pos' if m_dignity != 'Debilitated' else 'neg', category='Education')}</b> in your learning journey.")

    if m_dignity == 'Debilitated':
        base_score -= 10
        points.append("<b>Challenge:</b> Mercury is restricted, implying that consistent effort is needed for academic clarity.")
    elif m_dignity == 'Exalted':
        base_score += 10
        points.append("<b>Strength:</b> Mercury is powerful, providing sharp analytical and learning capabilities.")

    # 3. House-by-House Impacts
    area_map = {
        4: "Personal Learning",
        2: "Academic Speech",
        5: "Specialization",
        9: "Higher Research"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                  nature = get_planet_nature(planet)
                  outcome = get_house_outcome(house_num, type='pos' if planet in ['Mercury', 'Jupiter', 'Venus'] else 'neg', category='Education')
                  points.append(f"<b>{area}:</b> {planet}'s presence brings <b>{nature}</b> here, triggering <b>{outcome}</b>.")
                  if planet in ['Saturn', 'Rahu', 'Ketu']: base_score -= 5
                  found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers <b>{get_house_outcome(house_num, category='Education')}</b>.")

    # 4. Kendra Action Potential
    kendras = [p for p, pos in planetary_pos.items() if calculate_house(get_planet_sign(pos), asc_sign) in [1, 4, 7, 10] and p != 'Mandhi']
    if kendras:
        points.append(f"<b>Active Influences:</b> <b>{', '.join(kendras)}</b> are in central houses, actively impacting your educational focus.")

    # 5. Strategic Advice
    advice = "Focus on conceptual clarity and maintain a disciplined study routine for consistent academic success."
    if base_score < 55:
        advice = "Prioritize logical understanding over rote memorization during this phase."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_combinations(planetary_pos, asc_sign, target_houses, category='Education'))
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses, category='Education'))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses, category='Education'))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses, category='Education'))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Education"))

    # --- Dynamic Education Synthesis ---
    from astro_predictor_app.app.utils.astro_utils import get_dynamic_recommendations
    dynamic_insights = get_dynamic_recommendations(planetary_pos, asc_sign, 'Education')

    points.append("<b>Top Recommended Study Paths:</b>")
    
    lagna_recs = []
    if asc_sign in LAGNA_HOUSE_INDICATORS:
        lhi = LAGNA_HOUSE_INDICATORS[asc_sign]
        lagna_recs = lhi.get("Top_Study_Recommendations", [])

    # Priority 0: Nakshatra Pada Recommendation
    pada_rec = ""
    if nakshatra in PADA_TRAITS and pada in PADA_TRAITS[nakshatra]:
        pada_rec = PADA_TRAITS[nakshatra][pada].get('Education', '')

    # Combine and limit to exactly 5 (as requested by user)
    raw_combined = ([pada_rec] if pada_rec else []) + dynamic_insights + lagna_recs
    final_recs = []
    seen = set()
    for r in raw_combined:
        if r and r not in seen:
            final_recs.append(r)
            seen.add(r)
            if len(final_recs) >= 5: break

    for rec in final_recs:
        points.append(f"• {rec}")

    # Remedies Integration
    remedies = get_general_remedies("education")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
