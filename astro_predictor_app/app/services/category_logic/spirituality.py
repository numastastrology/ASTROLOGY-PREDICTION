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
    
    # Target Houses for Sprituality: 9 (Dharma), 12 (Moksha), 5 (Devotion), 8 (Occult)
    target_houses = [9, 12, 5, 8]
    
    base_score = 70
    
    # 1. Foundation
    h9_sign = get_sign_name((get_sign_number(asc_sign) + 9 - 1) % 12 or 12)
    h9_lord = get_lord(h9_sign)
    points.append(f"<b>Spiritual Foundation:</b> Your spiritual path is influenced by <b>{h9_sign}</b> energy, governed by <b>{h9_lord}</b> influences.")

    # 2. Key Significator (Jupiter for Dharma/Spirituality)
    jupiter_pos = planetary_pos.get('Jupiter', '')
    j_sign = get_planet_sign(jupiter_pos)
    j_house = calculate_house(j_sign, asc_sign)
    j_dignity = get_dignity('Jupiter', j_sign)
    points.append(f"<b>Dharma Significator:</b> Jupiter is in the {get_ordinal(j_house)} house in <b>{j_sign}</b>.")
    points.append(f"<b>Inner Growth:</b> Jupiter triggers <b>{get_house_outcome(j_house, type='pos' if j_dignity != 'Debilitated' else 'neg', category='Spirituality')}</b> in your spiritual journey.")

    # 3. House-by-House Impacts
    area_map = {
        9: "Dharma & Philosophy",
        12: "Moksha & Solitude",
        5: "Devotion & Mantra"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                  nature = get_planet_nature(planet)
                  outcome = get_house_outcome(house_num, type='pos' if planet in ['Jupiter', 'Saturn', 'Ketu'] else 'neg', category='Spirituality')
                  points.append(f"<b>{area}:</b> {planet}'s presence brings <b>{nature}</b> here, triggering <b>{outcome}</b>.")
                  found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers <b>{get_house_outcome(house_num, category='Spirituality')}</b>.")

    # 4. Strategic Advice
    advice = "Maintain a consistent spiritual practice and focus on selfless service for inner peace."
    if base_score < 60:
        advice = "Focus on basics and meditation during this reflective planetary phase."
    
    # --- Dynamic Spirituality Synthesis ---
    from astro_predictor_app.app.utils.astro_utils import get_dynamic_recommendations
    dynamic_insights = get_dynamic_recommendations(planetary_pos, asc_sign, 'Spirituality')

    points.append("<b>Top Recommended Spiritual Paths:</b>")
    
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
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses, category='Spirituality'))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses, category='Spirituality'))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses, category='Spirituality'))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Spirituality"))

    # Remedies Integration
    remedies = get_general_remedies("spirituality")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
