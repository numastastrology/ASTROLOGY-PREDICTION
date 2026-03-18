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
    
    # Target Houses for Enemies: 6 (Open Enemies/Debts), 7 (Opponents), 8 (Hidden Enemies)
    target_houses = [6, 7, 8]
    
    base_score = 65
    
    # 1. Foundation
    h6_sign = get_sign_name((get_sign_number(asc_sign) + 6 - 1) % 12 or 12)
    h6_lord = get_lord(h6_sign)
    points.append(f"<b>Conflict Foundation:</b> Your resistance to opposition is influenced by <b>{h6_sign}</b> energy, governed by <b>{h6_lord}</b> influences.")

    # 2. Key Significator (Mars for Courage/Conflict)
    mars_pos = planetary_pos.get('Mars', '')
    ma_sign = get_planet_sign(mars_pos)
    ma_house = calculate_house(ma_sign, asc_sign)
    ma_dignity = get_dignity('Mars', ma_sign)
    points.append(f"<b>Courage Significator:</b> Mars is in the {get_ordinal(ma_house)} house in <b>{ma_sign}</b>.")
    points.append(f"<b>Competitive Edge:</b> Mars triggers <b>{get_house_outcome(ma_house, type='pos' if ma_dignity != 'Debilitated' else 'neg', category='Legal')}</b> in your interaction with opponents.")

    # 3. House-by-House Impacts
    area_map = {
        6: "Open Resistance",
        7: "External Opponents",
        8: "Hidden Challenges"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                  nature = get_planet_nature(planet)
                  # Malefics in 6 are often good for winning over enemies
                  is_positive = (house_num == 6 and planet in ['Mars', 'Saturn', 'Rahu']) or planet == 'Jupiter'
                  outcome = get_house_outcome(house_num, type='pos' if is_positive else 'neg', category='Legal')
                  points.append(f"<b>{area}:</b> {planet}'s presence brings <b>{nature}</b> here, triggering <b>{outcome}</b>.")
                  found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers <b>{get_house_outcome(house_num, category='Legal')}</b>.")

    # 4. Strategic Advice
    advice = "Focus on diplomacy and strategic patience to overcome external challenges."
    if base_score < 60:
        advice = "Avoid unnecessary confrontations and focus on building strong internal defenses."
    
    # --- Dynamic Enemy Synthesis ---
    from astro_predictor_app.app.utils.astro_utils import get_dynamic_recommendations
    dynamic_insights = get_dynamic_recommendations(planetary_pos, asc_sign, 'Legal')

    points.append("<b>Top Recommended Conflict Resolution Strategies:</b>")
    
    lagna_recs = ["Strategic Diplomacy", "Legal Fortifications", "Patience & Perseverance"]
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
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses, category='Legal'))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses, category='Legal'))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses, category='Legal'))
    points.extend(analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Enemies & Competition"))

    # Remedies Integration
    remedies = get_general_remedies("legal")
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
