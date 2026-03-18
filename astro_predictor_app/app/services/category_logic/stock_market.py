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
    
    # Target Houses for Stock Market: 5 (Speculation), 11 (Gains), 2 (Wealth), 8 (Sudden Gains)
    target_houses = [5, 11, 2, 8]
    
    base_score = 55
    
    # 1. Foundation
    h5_sign = get_sign_name((get_sign_number(asc_sign) + 5 - 1) % 12 or 12)
    h5_lord = get_lord(h5_sign)
    points.append(f"<b>Speculative Foundation:</b> Your stock market and speculation path is influenced by <b>{h5_sign}</b> energy, governed by <b>{h5_lord}</b> influences.")

    # 2. Key Significators (Mercury for Logic/Trade, Rahu for Speculation)
    mercury_pos = planetary_pos.get('Mercury', '')
    m_sign = get_planet_sign(mercury_pos)
    m_house = calculate_house(m_sign, asc_sign)
    points.append(f"<b>Trading Significator:</b> Mercury (logic/trade) is in the {get_ordinal(m_house)} house in <b>{m_sign}</b>.")

    rahu_pos = planetary_pos.get('Rahu', '')
    r_house = calculate_house(get_planet_sign(rahu_pos), asc_sign)
    if r_house in [5, 8, 11]:
         points.append(f"<b>Speculative Trigger:</b> Rahu in the {get_ordinal(r_house)} house triggers high-risk, high-reward potential.")
         base_score += 10

    # 3. House-by-House Impacts
    area_map = {
        5: "Speculation Potential",
        11: "Market Gains",
        8: "Sudden Fluctuations"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                  nature = get_planet_nature(planet)
                  outcome = get_house_outcome(house_num, type='pos' if planet in ['Mercury', 'Jupiter', 'Rahu'] else 'neg', category='Finance')
                  points.append(f"<b>{area}:</b> {planet}'s presence brings <b>{nature}</b> here, triggering <b>{outcome}</b>.")
                  found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers <b>{get_house_outcome(house_num, category='Finance')}</b>.")

    # 4. Strategic Advice
    advice = "Focus on long-term investments rather than intra-day trading for better stability."
    if base_score < 50:
        advice = "Avoid major market exposure during this volatile planetary phase."
    
    # --- Dynamic Stock Synthesis ---
    from astro_predictor_app.app.utils.astro_utils import get_dynamic_recommendations
    dynamic_insights = get_dynamic_recommendations(planetary_pos, asc_sign, 'Finance')

    points.append("<b>Top Recommended Market Strategies:</b>")
    
    lagna_recs = ["Long-term Equity Focus", "Blue-chip Stocks", "Sectoral Funds"]
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
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses, category='Finance'))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses, category='Finance'))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses, category='Finance'))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Stock Market"))

    # Remedies Integration
    remedies = get_general_remedies("finance")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
