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
    
    # Target Houses for Vehicles: 4 (Conveyance), 11 (Gains), 2 (Family)
    target_houses = [4, 11, 2]
    
    base_score = 65
    
    # 1. Foundation
    h4_sign = get_sign_name((get_sign_number(asc_sign) + 4 - 1) % 12 or 12)
    h4_lord = get_lord(h4_sign)
    points.append(f"<b>Conveyance Foundation:</b> Your vehicle and comfort path is influenced by <b>{h4_sign}</b> energy, governed by <b>{h4_lord}</b> influences.")

    # 2. Key Significator (Venus for Vehicles/Luxury)
    venus_pos = planetary_pos.get('Venus', '')
    v_sign = get_planet_sign(venus_pos)
    v_house = calculate_house(v_sign, asc_sign)
    v_dignity = get_dignity('Venus', v_sign)
    points.append(f"<b>Luxury Significator:</b> Venus (planet of vehicles) is in the {get_ordinal(v_house)} house in <b>{v_sign}</b>.")
    points.append(f"<b>Vahan Sukh:</b> Venus triggers <b>{get_house_outcome(v_house, type='pos' if v_dignity != 'Debilitated' else 'neg', category='Vehicles')}</b> in your conveyance matters.")

    # 3. House-by-House Impacts
    area_map = {
        4: "Personal Vehicles",
        11: "Gains in Comfort",
        2: "Family Assets"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                  nature = get_planet_nature(planet)
                  outcome = get_house_outcome(house_num, type='pos' if planet in ['Venus', 'Moon', 'Jupiter'] else 'neg', category='Vehicles')
                  points.append(f"<b>{area}:</b> {planet}'s presence brings <b>{nature}</b> here, triggering <b>{outcome}</b>.")
                  found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers <b>{get_house_outcome(house_num, category='Vehicles')}</b>.")

    # 4. Strategic Advice
    advice = "Opt for vehicles that provide long-term reliability and ensure proper maintenance for safety."
    if base_score < 55:
        advice = "Exercise caution during vehicle purchases and focus on safety features."
    
    # --- Dynamic Vehicles Synthesis ---
    from astro_predictor_app.app.utils.astro_utils import get_dynamic_recommendations
    dynamic_insights = get_dynamic_recommendations(planetary_pos, asc_sign, 'Vehicles')

    points.append("<b>Top Recommended Vehicle Options:</b>")
    
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
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses, category='Vehicles'))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses, category='Vehicles'))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses, category='Vehicles'))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Vehicles"))

    # Remedies Integration
    remedies = get_general_remedies("vehicles")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
