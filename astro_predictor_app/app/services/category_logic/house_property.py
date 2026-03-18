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
    
    # Target Houses for House Property: 4 (Home), 11 (Gains), 2 (Family)
    target_houses = [4, 11, 2]
    
    base_score = 60
    
    # 1. Foundation
    h4_sign = get_sign_name((get_sign_number(asc_sign) + 4 - 1) % 12 or 12)
    h4_lord = get_lord(h4_sign)
    points.append(f"<b>Inherent Assets Foundation:</b> Your property path is influenced by <b>{h4_sign}</b> energy, governed by <b>{h4_lord}</b> influences.")

    # 2. Key Significator (Mars for Property/Land)
    mars_pos = planetary_pos.get('Mars', '')
    ma_sign = get_planet_sign(mars_pos)
    ma_house = calculate_house(ma_sign, asc_sign)
    ma_dignity = get_dignity('Mars', ma_sign)
    points.append(f"<b>Property Significator:</b> Mars (planet of land) is in the {get_ordinal(ma_house)} house in <b>{ma_sign}</b>.")
    points.append(f"<b>Asset Accumulation:</b> Mars triggers <b>{get_house_outcome(ma_house, type='pos' if ma_dignity != 'Debilitated' else 'neg', category='Property')}</b> in your property matters.")

    if ma_dignity == 'Debilitated':
        base_score -= 10
        points.append("<b>Challenge:</b> Mars is restricted, implying that property acquisitions might face temporary delays or hurdles.")
    elif ma_dignity == 'Exalted':
        base_score += 10
        points.append("<b>Strength:</b> Mars is powerful, favoring quick and stable property gains.")

    # 3. House-by-House Impacts
    area_map = {
        4: "Home & Comforts",
        11: "Asset Gains",
        2: "Family Support"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                  nature = get_planet_nature(planet)
                  outcome = get_house_outcome(house_num, type='pos' if planet in ['Mars', 'Venus', 'Jupiter'] else 'neg', category='Property')
                  points.append(f"<b>{area}:</b> {planet}'s presence brings <b>{nature}</b> here, triggering <b>{outcome}</b>.")
                  if planet in ['Saturn', 'Rahu', 'Ketu']: base_score -= 10
                  found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers <b>{get_house_outcome(house_num, category='Property')}</b>.")

    # 4. Strengths & Challenges Summary
    challenges = []
    stability = []
    for planet in ['Mars', 'Venus', h4_lord]:
        p_pos = planetary_pos.get(planet, '')
        if not p_pos: continue
        p_sign = get_planet_sign(p_pos)
        dig = get_dignity(planet, p_sign)
        if dig == 'Debilitated' or calculate_house(p_sign, asc_sign) in [6, 8, 12]:
            challenges.append(planet)
        elif dig == 'Exalted' or get_lord(p_sign) == planet:
            stability.append(planet)

    if challenges:
        points.append(f"<b>Challenges:</b> <b>{', '.join(challenges)}</b> show some asset hurdles, requiring thorough verification of documents.")
    if stability:
        points.append(f"<b>Stability:</b> <b>{', '.join(stability)}</b> are well-placed, providing a favorable influence for domestic stability.")

    # 5. Kendra Action Potential
    kendras = [p for p, pos in planetary_pos.items() if calculate_house(get_planet_sign(pos), asc_sign) in [1, 4, 7, 10] and p != 'Mandhi']
    if kendras:
        points.append(f"<b>Active Influences:</b> <b>{', '.join(kendras)}</b> are in central houses, actively impacting your property decisions.")

    # 6. Strategic Advice
    advice = "Ensure all property documents are legally sound and focus on stable long-term investments."
    if base_score < 50:
        advice = "Defer major property purchases until more favorable planetary periods are active."
    
    # --- Dynamic Property Synthesis ---
    from astro_predictor_app.app.utils.astro_utils import get_dynamic_recommendations
    dynamic_insights = get_dynamic_recommendations(planetary_pos, asc_sign, 'Property')

    points.append("<b>Top Recommended Property Asset Paths:</b>")
    
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

    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses, category='Property'))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses, category='Property'))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses, category='Property'))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="House Property"))

    # Remedies Integration
    remedies = get_general_remedies("property")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
