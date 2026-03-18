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
    
    # Target Houses for Foreign: 12 (Foreign Lands), 9 (Long Distance), 7 (Public Deals)
    target_houses = [12, 9, 7]
    
    base_score = 60
    
    # 1. Foundation
    h12_sign = get_sign_name((get_sign_number(asc_sign) + 12 - 1) % 12 or 12)
    h12_lord = get_lord(h12_sign)
    points.append(f"<b>Foreign Connection Foundation:</b> Your foreign settlement path is influenced by <b>{h12_sign}</b> energy, governed by <b>{h12_lord}</b> influences.")

    # 2. Key Significator (Rahu/Saturn for Foreign travel/stay)
    rahu_pos = planetary_pos.get('Rahu', '')
    r_sign = get_planet_sign(rahu_pos)
    r_house = calculate_house(r_sign, asc_sign)
    points.append(f"<b>Primary Significator:</b> Rahu (planet of foreign lands) is in the {get_ordinal(r_house)} house in <b>{r_sign}</b>.")
    points.append(f"<b>Travel Indicator:</b> Rahu triggers <b>{get_house_outcome(r_house, type='pos' if r_house in [7, 9, 12] else 'neg', category='Travel')}</b> in your foreign-related endeavors.")

    # 3. House-by-House Impacts
    area_map = {
        12: "Foreign Residence",
        9: "Long Travel",
        7: "External Interactions"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                  nature = get_planet_nature(planet)
                  outcome = get_house_outcome(house_num, type='pos' if planet in ['Jupiter', 'Venus', 'Rahu'] else 'neg', category='Travel')
                  points.append(f"<b>{area}:</b> {planet}'s presence brings <b>{nature}</b> here, triggering <b>{outcome}</b>.")
                  if planet in ['Saturn', 'Mars', 'Ketu']: base_score -= 5 # Less penalty as malefic often cause displacement
                  found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers <b>{get_house_outcome(house_num, category='Travel')}</b>.")

    # 4. Strengths & Challenges Summary
    challenges = []
    stability = []
    for planet in ['Rahu', h12_lord]:
        p_pos = planetary_pos.get(planet, '')
        if not p_pos: continue
        p_sign = get_planet_sign(p_pos)
        dig = get_dignity(planet, p_sign)
        if calculate_house(p_sign, asc_sign) not in [7, 9, 12]:
            challenges.append(planet)
        else:
            stability.append(planet)

    if challenges:
        points.append(f"<b>Challenges:</b> <b>{', '.join(challenges)}</b> show some restrictions for permanent settlement, necessitating clear documentation.")
    if stability:
        points.append(f"<b>Stability:</b> <b>{', '.join(stability)}</b> are well-placed, providing a favorable path for international ventures.")

    # 5. Kendra Action Potential
    kendras = [p for p, pos in planetary_pos.items() if calculate_house(get_planet_sign(pos), asc_sign) in [1, 4, 7, 10] and p != 'Mandhi']
    if kendras:
        points.append(f"<b>Active Influences:</b> <b>{', '.join(kendras)}</b> are in central houses, actively driving your decisions regarding displacement.")

    # 6. Strategic Advice
    advice = "Ensure all legal documentation is thorough and plan travels during favorable planetary sub-periods."
    if base_score < 50:
        advice = "Re-evaluate long-term settlement plans and consider shorter stays initially."
    
    # --- Dynamic Travel Synthesis ---
    from astro_predictor_app.app.utils.astro_utils import get_dynamic_recommendations
    dynamic_insights = get_dynamic_recommendations(planetary_pos, asc_sign, 'Travel')

    points.append("<b>Key Travel & Settlement Insights:</b>")
    
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
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses, category='Travel'))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses, category='Travel'))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses, category='Travel'))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Foreign Settlement"))

    # Remedies Integration
    remedies = get_general_remedies("travel")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
