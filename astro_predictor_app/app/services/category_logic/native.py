from astro_predictor_app.app.utils.astro_utils import (
    get_sign_number, get_sign_name, get_planet_sign, calculate_house, get_lord,
    get_planet_nature, get_house_outcome, get_ordinal, get_dignity as utils_get_dignity,
    analyze_planetary_aspects, analyze_transits, analyze_jamakkol, analyze_dasa_bhukti_detailed
)
from astro_predictor_app.app.utils.remedy_utils import get_general_remedies, get_dasa_remedies

def analyze(birth_details, chart_data, dasa_info=None):
    points = []
    asc_sign = chart_data.get('ascendant', '')
    planetary_pos = chart_data.get('planetary_positions', {})
    transit_pos = chart_data.get('transit_positions', {})
    jamakkol_data = chart_data.get('jamakkol', {})
    nakshatra = chart_data.get('nakshatra', 'Unknown')
    pada = chart_data.get('pada', 'Unknown')
    
    base_score = 60
    
    # 1. Ascendant (Lagna)
    h1_lord = get_lord(asc_sign)
    points.append(f"<b>Ascendant (Lagna):</b> You are born under the **{asc_sign} Ascendant**, which characterizes your physical vitality and general outlook on life.")
    points.append(f"<b>Ruling Planet:</b> Your ruling planet is **{h1_lord}**, whose position in the chart significantly influences your personality.")

    # 2. Nature (Element-based)
    asc_num = get_sign_number(asc_sign)
    if asc_num in [1, 5, 9]:
        element = "Fire"
        nature_desc = "energetic, passionate, and action-oriented"
    elif asc_num in [2, 6, 10]:
        element = "Earth"
        nature_desc = "practical, stable, and grounded"
    elif asc_num in [3, 7, 11]:
        element = "Air"
        nature_desc = "intellectual, communicative, and socially adaptable"
    elif asc_num in [4, 8, 12]:
        element = "Water"
        nature_desc = "intuitive, emotional, and deeply sensitive"
    else:
        element = "Unknown"
        nature_desc = "unique"
    
    points.append(f"<b>Nature:</b> As an **{element} sign** ascendant, you are **{nature_desc}**.")

    # 3. Moon Sign (Rasi) & Nakshatra
    moon_pos = planetary_pos.get('Moon', '')
    moon_sign = get_planet_sign(moon_pos)
    points.append(f"<b>Moon Sign (Rasi):</b> Your Moon sign is **{moon_sign}**, indicating your emotional core and mental temperament.")
    
    moon_lord = get_lord(moon_sign)
    points.append(f"<b>Emotional Nature:</b> Governed by the Moon in **{moon_sign}**, your mental focus is influenced by **{moon_lord}** energy.")
    points.append(f"<b>Star (Nakshatra):</b> You were born under the **{nakshatra} Nakshatra**, which adds specific nuances to your moon sign traits.")
    points.append(f"<b>Pada:</b> Born in **{nakshatra} Pada {pada}**, giving a specific direction to your soul's purpose.")

    # 4. Sun Sign
    sun_pos = planetary_pos.get('Sun', '')
    sun_sign = get_planet_sign(sun_pos)
    points.append(f"<b>Sun Sign:</b> Your Soul Sign (Sun) is **{sun_sign}**, representing your ego, authority, and inner vitality.")

    # 5. Planetary Dignities (Challenges & Stability)
    challenges = []
    stability = []
    
    for planet, pos_str in planetary_pos.items():
        if planet in ['Mandhi', 'Rahu', 'Ketu']: continue
        p_sign = get_planet_sign(pos_str)
        # Check dignity using utils function if possible, or string cues
        is_debil = "(D)" in pos_str
        # 'Stability' refers to own sign or exaltation
        is_own = h1_lord == planet if p_sign == asc_sign else (get_lord(p_sign) == planet)
        is_exalted = "Exalted" in str(utils_get_dignity(planet, p_sign)) # utils_get_dignity is a safe bet if updated
        
        if is_debil:
            challenges.append(planet)
        if is_own or is_exalted:
            stability.append(planet)
            
    if challenges:
        points.append(f"<b>Challenges:</b> **{', '.join(challenges)}** are debilitated or restricted, suggesting areas where you may need to put in extra effort.")
        base_score -= (len(challenges) * 5)
    
    if stability:
        points.append(f"<b>Stability:</b> **{', '.join(stability)}** are well-placed (own/exalted), providing stability and consistent results.")
        base_score += (len(stability) * 5)

    # 6. Action Potential (Kendras: 1, 4, 7, 10)
    kendras = []
    for planet, pos_str in planetary_pos.items():
        if planet == 'Mandhi': continue
        p_sign = get_planet_sign(pos_str)
        p_house = calculate_house(p_sign, asc_sign)
        if p_house in [1, 4, 7, 10]:
            kendras.append(planet)
            
    if kendras:
        points.append(f"<b>Action Potential:</b> **{', '.join(kendras)}** are in Kendra houses (Angles), making them very active and influential in your life.")

    # 7. House Summaries (Wisdom, Discipline, etc. style)
    area_map = {
        "Jupiter": "Wisdom",
        "Saturn": "Discipline",
        "Mars": "Energy",
        "Venus": "Relationships",
        "Mercury": "Communication",
        "Sun": "Vitality",
        "Moon": "Mindset"
    }
    
    for planet, area in area_map.items():
        pos_str = planetary_pos.get(planet, '')
        p_sign = get_planet_sign(pos_str)
        p_house = calculate_house(p_sign, asc_sign)
        if p_house:
            target_area = get_house_outcome(p_house)
            points.append(f"<b>{area}:</b> {planet} in the {get_ordinal(p_house)} house influences your **{target_area}**.")

    # 8. Malefic/Benefic House 1 Specifics (from Photo 1 example "Venus in 1st house...")
    # This is already covered by the loop above, but we can add more if needed.

    # 9. Dasa/Transit (Keep for completeness but keep it brief as per style)
    dasa_points = analyze_dasa_bhukti_detailed(dasa_info, {}, category_name="Character")
    points.extend(dasa_points[:2]) # Only top 2 for brevity

    # Remedies Integration
    remedies = get_general_remedies("health") # General health/native remedies
    if dasa_info:
        remedies.extend(get_dasa_remedies(dasa_info.get('dasa', {}).get('lord')))

    return {
        "score": max(5, min(int(base_score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
