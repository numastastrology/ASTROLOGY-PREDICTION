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
    
    # Target Houses for Promotion: 10 (Career), 11 (Gains), 6 (Service), 1 (Status)
    target_houses = [10, 11, 6, 1]
    
    base_score = 60
    
    # 1. Foundation
    h10_sign = get_sign_name((get_sign_number(asc_sign) + 10 - 1) % 12 or 12)
    h10_lord = get_lord(h10_sign)
    points.append(f"<b>Progress Foundation:</b> Your promotional path is influenced by <b>{h10_sign}</b> energy, governed by <b>{h10_lord}</b> influences.")

    # 2. Key Significator (Sun for Authority/Status)
    sun_pos = planetary_pos.get('Sun', '')
    s_sign = get_planet_sign(sun_pos)
    s_house = calculate_house(s_sign, asc_sign)
    s_dignity = get_dignity('Sun', s_sign)
    points.append(f"<b>Authority Significator:</b> Sun (planet of status) is in the {get_ordinal(s_house)} house in <b>{s_sign}</b>.")
    points.append(f"<b>Recognition Potential:</b> Sun triggers <b>{get_house_outcome(s_house, type='pos' if s_dignity != 'Debilitated' else 'neg', category='Career')}</b> in your career progression.")

    # 3. Strategic Advice
    advice = "Maintain consistent performance and build strong connections with authority figures for better growth."
    if base_score < 50:
        advice = "Focus on specialized skill-building and wait for more favorable planetary transits for promotion requests."
    
    # --- Dynamic Promotion Synthesis ---
    from astro_predictor_app.app.utils.astro_utils import get_dynamic_recommendations
    dynamic_insights = get_dynamic_recommendations(planetary_pos, asc_sign, 'Career')

    points.append("<b>Top Recommended Growth Strategies:</b>")
    
    lagna_recs = ["Authority Networking", "Skill Specialization", "Strategic Leadership"]
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
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses, category='Career'))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses, category='Career'))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses, category='Career'))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Promotion & Growth"))

    # Remedies Integration
    remedies = get_general_remedies("career")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
