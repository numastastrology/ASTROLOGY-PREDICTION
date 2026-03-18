from astro_predictor_app.app.utils.astro_utils import (
    get_sign_number, get_sign_name, get_planet_sign, calculate_house, get_lord,
    get_planet_nature, get_house_outcome, get_ordinal, get_dignity,
    analyze_planetary_aspects, analyze_transits, analyze_jamakkol, analyze_dasa_bhukti_detailed
)
from astro_predictor_app.app.utils.remedy_utils import get_general_remedies, get_dasa_remedies
from astro_predictor_app.app.utils.description_utils import LAGNA_HOUSE_INDICATORS

def analyze(birth_details, chart_data, dasa_info=None):
    points = []
    asc_sign = chart_data.get('ascendant', '')
    planetary_pos = chart_data.get('planetary_positions', {})
    transit_pos = chart_data.get('transit_positions', {})
    jamakkol_data = chart_data.get('jamakkol', {})
    
    # Target Houses for Finance: 2 (Wealth), 11 (Gains), 5 (Speculation), 9 (Fortune)
    target_houses = [2, 11, 5, 9]
    
    base_score = 60
    
    # 1. Foundation
    h2_sign = get_sign_name((get_sign_number(asc_sign) + 2 - 1) % 12 or 12)
    h2_lord = get_lord(h2_sign)
    points.append(f"<b>Financial Foundation:</b> Your wealth potential is influenced by <b>{h2_sign}</b> energy, governed by <b>{h2_lord}</b> influences.")

    if asc_sign in LAGNA_HOUSE_INDICATORS:
        indicators = LAGNA_HOUSE_INDICATORS[asc_sign].get("Finance", [])
        points.extend(indicators)

    # 2. Key Significator (Jupiter for Wealth)
    jupiter_pos = planetary_pos.get('Jupiter', '')
    j_sign = get_planet_sign(jupiter_pos)
    j_house = calculate_house(j_sign, asc_sign)
    j_dignity = get_dignity('Jupiter', j_sign)
    points.append(f"<b>Wealth Significator:</b> Jupiter is in the {get_ordinal(j_house)} house in <b>{j_sign}</b>.")
    points.append(f"<b>Prosperity Potential:</b> Jupiter triggers <b>{get_house_outcome(j_house, type='pos' if j_dignity != 'Debilitated' else 'neg', category='Finance')}</b> in your life.")

    if j_dignity == 'Debilitated':
        base_score -= 10
        points.append("<b>Challenge:</b> Jupiter is restricted, suggesting success through cautious financial management.")
    elif j_dignity == 'Exalted':
        base_score += 10
        points.append("<b>Strength:</b> Jupiter is powerful, naturally favoring wealth accumulation and stability.")

    # 3. House-by-House Impacts
    area_map = {
        2: "Liquid Assets",
        11: "Income Gains",
        5: "Speculative Wealth"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                  nature = get_planet_nature(planet)
                  outcome = get_house_outcome(house_num, type='pos' if planet in ['Jupiter', 'Venus', 'Mercury'] else 'neg', category='Finance')
                  points.append(f"<b>{area}:</b> {planet}'s presence brings <b>{nature}</b> here, triggering <b>{outcome}</b>.")
                  if planet in ['Saturn', 'Rahu', 'Ketu']: base_score -= 5
                  found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers <b>{get_house_outcome(house_num, category='Finance')}</b>.")

    # 4. Strategic Advice
    advice = "Maintain a diversified portfolio and focus on consistent savings to build long-term wealth."
    if base_score < 50:
        advice = "Avoid high-risk speculative investments during this planetary phase."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses, category='Finance'))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses, category='Finance'))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses, category='Finance'))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Finance"))

    # --- Dynamic Finance Synthesis ---
    from astro_predictor_app.app.utils.astro_utils import get_dynamic_recommendations
    dynamic_insights = get_dynamic_recommendations(planetary_pos, asc_sign, 'Finance')

    points.append("<b>Top Recommended Financial Strategies:</b>")
    
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

    # Remedies Integration
    remedies = get_general_remedies("finance")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
