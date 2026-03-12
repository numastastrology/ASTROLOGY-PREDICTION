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
    
    # Target Houses for Vehicles: 4 (Vehicles/Conveyance), 11 (Gains), 2 (Wealth)
    target_houses = [4, 11, 2]
    
    base_score = 60
    
    # 1. Foundation
    h4_sign = get_sign_name((get_sign_number(asc_sign) + 4 - 1) % 12 or 12)
    h4_lord = get_lord(h4_sign)
    points.append(f"<b>Conveyance Foundation:</b> Your vehicle and comfort path is influenced by **{h4_sign}** energy, governed by **{h4_lord}**.")

    # 2. Key Significator (Venus for Vehicles/Luxury)
    venus_pos = planetary_pos.get('Venus', '')
    v_sign = get_planet_sign(venus_pos)
    v_house = calculate_house(v_sign, asc_sign)
    v_dignity = get_dignity('Venus', v_sign)
    points.append(f"<b>Luxury Significator:</b> Venus (planet of conveyance) is in the {get_ordinal(v_house)} house in **{v_sign}**.")
    points.append(f"<b>Vehicle Comfort:</b> Venus triggers **{get_house_outcome(v_house, type='pos' if v_dignity != 'Debilitated' else 'neg')}** in your personal life.")

    if v_dignity == 'Debilitated':
        base_score -= 10
        points.append("<b>Challenge:</b> Venus is restricted here, requiring more conscious care regarding vehicle maintenance.")
    elif v_dignity == 'Exalted':
        base_score += 10
        points.append("<b>Strength:</b> Venus is powerful, enhancing luxury and ease of vehicle acquisition.")

    # 3. House-by-House Impacts
    area_map = {
        4: "Vehicle Ownership",
        11: "Gains in Comfort",
        2: "Financial Stability"
    }
    
    for house_num, area in area_map.items():
        found = False
        for planet, pos_str in planetary_pos.items():
             if planet == 'Mandhi': continue
             p_sign = get_planet_sign(pos_str)
             p_house = calculate_house(p_sign, asc_sign)
             if p_house == house_num:
                 nature = get_planet_nature(planet)
                 outcome = get_house_outcome(house_num, type='pos' if planet in ['Venus', 'Jupiter', 'Mercury'] else 'neg')
                 points.append(f"<b>{area}:</b> {planet}'s presence brings **{nature}** here, triggering **{outcome}**.")
                 if planet in ['Saturn', 'Mars', 'Rahu', 'Ketu']: base_score -= 10
                 found = True
        if not found:
             points.append(f"<b>{area}:</b> The {get_ordinal(house_num)} house energy triggers **{get_house_outcome(house_num)}**.")

    # 4. Strengths & Challenges Summary
    challenges = []
    stability = []
    for planet in ['Venus', h4_lord]:
        p_pos = planetary_pos.get(planet, '')
        if not p_pos: continue
        p_sign = get_planet_sign(p_pos)
        dig = get_dignity(planet, p_sign)
        if dig == 'Debilitated' or calculate_house(p_sign, asc_sign) in [6, 8, 12]:
            challenges.append(planet)
        elif dig == 'Exalted' or get_lord(p_sign) == planet:
            stability.append(planet)

    if challenges:
        points.append(f"<b>Challenges:</b> **{', '.join(challenges)}** show some hurdles in conveyance, requiring careful planning.")
    if stability:
        points.append(f"<b>Stability:</b> **{', '.join(stability)}** are well-placed, providing a favorable influence for vehicle acquisition.")

    # 5. Kendra Action Potential
    kendras = [p for p, pos in planetary_pos.items() if calculate_house(get_planet_sign(pos), asc_sign) in [1, 4, 7, 10] and p != 'Mandhi']
    if kendras:
        points.append(f"<b>Active Influences:</b> **{', '.join(kendras)}** are in central houses, actively driving your conveyance status.")

    # 6. Strategic Advice
    advice = "Maintain vehicles regularly and focus on safe, reliable options for daily travel."
    if base_score < 50:
        advice = "Monitor vehicle-related expenses closely and wait for favorable planetary and Dasa periods."
    points.append(f"<b>Strategic Recommendation:</b> {advice}")

    # Standardized Logic
    points.extend(analyze_planetary_aspects(planetary_pos, asc_sign, target_houses))
    points.extend(analyze_transits(transit_pos, asc_sign, target_houses))
    points.extend(analyze_jamakkol(jamakkol_data, asc_sign, target_houses))
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
