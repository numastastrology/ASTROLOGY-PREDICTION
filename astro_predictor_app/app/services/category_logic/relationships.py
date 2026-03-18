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
    
    # Target Houses for Relationships: 7 (Spouse), 2 (Family), 11 (Social), 1 (Self)
    target_houses = [7, 2, 11, 1]
    
    base_score = 65
    
    # 1. Foundation
    h7_sign = get_sign_name((get_sign_number(asc_sign) + 7 - 1) % 12 or 12)
    h7_lord = get_lord(h7_sign)
    points.append(f"<b>Relational Foundation:</b> Your partnership path is influenced by <b>{h7_sign}</b> energy, governed by <b>{h7_lord}</b> influences.")

    if asc_sign in LAGNA_HOUSE_INDICATORS:
        indicators = LAGNA_HOUSE_INDICATORS[asc_sign].get("Relationships", [])
        points.extend(indicators)

    # 2. Key Significator (Venus for Love/Partnership)
    venus_pos = planetary_pos.get('Venus', '')
    v_sign = get_planet_sign(venus_pos)
    v_house = calculate_house(v_sign, asc_sign)
    v_dignity = get_dignity('Venus', v_sign)
    points.append(f"<b>Harmony Significator:</b> Venus is in the {get_ordinal(v_house)} house in <b>{v_sign}</b>.")
    points.append(f"<b>Relational Quality:</b> Venus triggers <b>{get_house_outcome(v_house, type='pos' if v_dignity != 'Debilitated' else 'neg', category='Relationships')}</b> in your interactions.")

    if v_dignity == 'Debilitated':
        base_score -= 10
        points.append("<b>Challenge:</b> Venus is restricted, suggesting that harmony requires extra effort in communication and understanding.")
    elif v_dignity == 'Exalted':
        base_score += 10
        points.append("<b>Strength:</b> Venus is powerful, favoring smooth relationships and natural charm.")

    # 3. House-by-House Impacts
    area_map = {
        7: "Partnership Engagement",
        2: "Family Harmony",
        11: "Social Connections"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                  nature = get_planet_nature(planet)
                  outcome = get_house_outcome(house_num, type='pos' if planet in ['Venus', 'Jupiter', 'Moon'] else 'neg', category='Relationships')
                  points.append(f"<b>{area}:</b> {planet}'s presence brings <b>{nature}</b> here, triggering <b>{outcome}</b>.")
                  if planet in ['Saturn', 'Mars', 'Rahu', 'Ketu']: base_score -= 5
                  found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers <b>{get_house_outcome(house_num, category='Relationships')}</b>.")

    # 4. Strategic Advice
    advice = "Maintain open communication and prioritize mutual respect to foster long-lasting relational harmony."
    if base_score < 55:
        advice = "Practice patience and focus on building emotional understanding with partners."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses, category='Relationships'))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses, category='Relationships'))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses, category='Relationships'))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Relationships"))

    # --- Dynamic Relationship Synthesis ---
    from astro_predictor_app.app.utils.astro_utils import get_dynamic_recommendations
    dynamic_insights = get_dynamic_recommendations(planetary_pos, asc_sign, 'Relationships')

    points.append("<b>Top Recommended Relational Strategies:</b>")
    
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
    remedies = get_general_remedies("relationships")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
