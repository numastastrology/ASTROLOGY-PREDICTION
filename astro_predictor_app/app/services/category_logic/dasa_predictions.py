from astro_predictor_app.app.utils.astro_utils import (
    get_planet_sign, calculate_house, get_lord, get_planet_nature, 
    get_house_outcome, get_ordinal, get_aspects, get_ruled_houses, 
    get_relationship, get_dignity, get_house_description
)
from astro_predictor_app.app.utils.remedy_utils import get_dasa_remedies

def analyze(birth_details, chart_data, dasa_info=None):
    points = []
    if not dasa_info:
        return {"score": 0, "points": ["No Dasa information available."], "remedies": []}
    
    asc_sign = chart_data.get('ascendant', '')
    planetary_pos = chart_data.get('planetary_positions', {})
    
    d_lord = dasa_info.get('dasa', {}).get('lord')
    b_lord = dasa_info.get('bhukti', {}).get('lord')
    a_lord = dasa_info.get('antara', {}).get('lord')
    
    # 1. Header Info (1 point)
    points.append(f"<b>CURRENT PERIOD:</b> {d_lord} Major Cycle / {b_lord} Sub-Cycle / {a_lord} Minor Cycle")
    
    # --- Mahadasa Lord Analysis (Approx 5 points) ---
    d_sign = get_planet_sign(planetary_pos.get(d_lord, ''))
    d_house = calculate_house(d_sign, asc_sign)
    d_nature = get_planet_nature(d_lord)
    d_ruled = get_ruled_houses(d_lord, asc_sign)
    d_dignity = get_dignity(d_lord, d_sign)
    
    points.append(f"<b>1. Main Period Lordship:</b> {d_lord} rules your {', '.join([get_ordinal(h) for h in d_ruled])} houses, focusing your destiny on these areas.")
    points.append(f"<b>2. Main Period Nature:</b> {d_lord} is active, bringing <b>{d_nature}</b> to the forefront of your long-term life trajectory.")
    points.append(f"<b>3. House Impact:</b> Positioned in the {get_ordinal(d_house)} house, it triggers <b>{get_house_outcome(d_house, type='pos' if d_dignity != 'Debilitated' else 'neg')}</b>.")
    points.append(f"<b>4. Global Influence:</b> This major cycle defines your identity and social standing through <b>{get_house_description(d_house)}</b>.")
    
    # Aspects of Mahadasa Lord (3 points)
    d_aspects = get_aspects(d_lord, d_sign, asc_sign)
    for i, ah in enumerate(d_aspects[:3]):
        outcome = get_house_outcome(ah, type='pos' if d_lord in ['Jupiter', 'Venus', 'Mercury', 'Moon'] else 'neg')
        points.append(f"<b>5.{i+1} Aspect Influence:</b> {d_lord}'s gaze on the {get_ordinal(ah)} house drives <b>{outcome}</b>.")

    # --- Bhukti Lord Analysis (Approx 5 points) ---
    b_sign = get_planet_sign(planetary_pos.get(b_lord, ''))
    b_house = calculate_house(b_sign, asc_sign)
    b_nature = get_planet_nature(b_lord)
    b_ruled = get_ruled_houses(b_lord, asc_sign)
    b_dignity = get_dignity(b_lord, b_sign)
    
    points.append(f"<b>6. Sub-Period Lordship:</b> {b_lord} governs the {', '.join([get_ordinal(h) for h in b_ruled])} houses, activating these specific life sectors now.")
    points.append(f"<b>7. Sub-Period Nature:</b> Expect <b>{b_nature}</b> to manifest intensely in your daily decisions and current mood.")
    points.append(f"<b>8. Sub-Period House:</b> {b_lord} in the {get_ordinal(b_house)} house triggers <b>{get_house_outcome(b_house, type='pos' if b_dignity != 'Debilitated' else 'neg')}</b>.")
    points.append(f"<b>9. Current Mood:</b> Your inner focus is currently shifting toward <b>{get_house_description(b_house)}</b>.")

    # Aspects of Bhukti Lord (3 points)
    b_aspects = get_aspects(b_lord, b_sign, asc_sign)
    for i, ah in enumerate(b_aspects[:3]):
        outcome = get_house_outcome(ah, type='pos' if b_lord in ['Jupiter', 'Venus'] else 'neg')
        points.append(f"<b>10.{i+1} Current Phase Effect:</b> {b_lord}'s impact on your {get_ordinal(ah)} house triggers <b>{outcome}</b>.")

    # --- Dasa-Bhukti Relationship (1 point) ---
    rel = get_relationship(d_lord, b_lord)
    points.append(f"<b>11. Period Harmony:</b> The relationship between your Major and Sub lords is <b>{rel}</b>, indicating how smoothly these energies blend.")

    # --- Life Area Specifics (4 points) ---
    points.append(f"<b>12. Career Impact:</b> The current planetary mix emphasizes <b>{get_house_outcome(10, type='pos' if 'Jupiter' in [d_lord, b_lord] else 'neg')}</b> at work.")
    points.append(f"<b>13. Financial Impact:</b> Wealth potential is currently defined by <b>{get_house_outcome(2, type='pos' if 'Venus' in [d_lord, b_lord] or 'Jupiter' in [d_lord, b_lord] else 'neg')}</b>.")
    points.append(f"<b>14. Health Impact:</b> Physical vitality is influenced by <b>{get_house_outcome(1, type='pos' if 'Sun' in [d_lord, b_lord] else 'neg')}</b>.")
    points.append(f"<b>15. Relationship Impact:</b> Interaction with others is governed by <b>{get_house_outcome(7, type='pos' if 'Venus' in [d_lord, b_lord] else 'neg')}</b>.")

    # --- Antara Lord brief (2 points) ---
    if a_lord:
        a_sign = get_planet_sign(planetary_pos.get(a_lord, ''))
        a_house = calculate_house(a_sign, asc_sign)
        points.append(f"<b>16. Immediate Focus:</b> The minor cycle of {a_lord} in the {get_ordinal(a_house)} house emphasizes <b>{get_house_outcome(a_house)}</b>.")
        points.append(f"<b>17. Mental State:</b> {a_lord}'s nature of <b>{get_planet_nature(a_lord)}</b> is currently influencing your fleeting thoughts.")

    # --- Strategic Recommendations (3 points) ---
    if b_lord in ['Saturn', 'Rahu', 'Ketu']:
        r1 = "Focus on extreme discipline and avoid sudden, unconventional shortcuts."
        r2 = "Handle setbacks with patience; these are transformative opportunities in disguise."
    else:
        r1 = "This is a period for growth and bold initiatives; capitalize on new openings."
        r2 = "Invest in long-term assets and expand your social or professional network."
    
    points.append(f"<b>18. Primary Action:</b> {r1}")
    points.append(f"<b>19. Mindset Shift:</b> {r2}")
    points.append(f"<b>20. Final Guidance:</b> Align your daily routine with {b_lord}'s preferred energy of <b>{get_planet_nature(b_lord)}</b>.")

    # --- Scoring ---
    score = 60
    if d_house in [6, 8, 12]: score -= 10
    if b_house in [6, 8, 12]: score -= 15
    if b_lord in ['Saturn', 'Rahu', 'Ketu'] and b_house in [6, 8, 12]: score -= 10
    
    # --- Remedies (Expansion to >15 points) ---
    remedies = []
    remedies.extend(get_dasa_remedies(d_lord))
    remedies.extend(get_dasa_remedies(b_lord))
    
    # If still short of 15, add general harmony
    if len(remedies) < 18:
        remedies.append("Offer a ghee lamp in your prayer area every evening for general harmony.")
        remedies.append("Feed stray animals on Saturdays to balance planetary energies.")
        remedies.append("Meditate daily for 15 minutes to align your mind with your Dasa cycle.")
        remedies.append("Practice gratitude daily to attract positive energy from the universe.")
    
    return {
        "score": max(5, min(int(score), 100)),
        "points": list(dict.fromkeys(points)),
        "remedies": list(dict.fromkeys(remedies))
    }
