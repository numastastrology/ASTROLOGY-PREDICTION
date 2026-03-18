from astro_predictor_app.app.utils.astro_utils import (
    get_sign_number, get_sign_name, get_planet_sign, calculate_house, get_lord,
    get_planet_nature, get_house_outcome, get_ordinal, get_dignity, get_nak_info
)
from astro_predictor_app.app.utils.description_utils import (
    LAGNA_TRAITS, MOON_TRAITS, NAKSHATRA_TRAITS, LAGNA_HOUSE_INDICATORS
)

def analyze(birth_details, chart_data, dasa_info=None):
    points = []
    asc_sign = chart_data.get('ascendant', '')
    planetary_pos = chart_data.get('planetary_positions', {})
    
    # 1. Foundation & Lagna Traits
    h1_lord = get_lord(asc_sign)
    points.append(f"<b>Identity Foundation:</b> Your core personality is governed by <b>{asc_sign}</b> energy and <b>{h1_lord}</b> influences.")
    
    if asc_sign in LAGNA_TRAITS:
        t = LAGNA_TRAITS[asc_sign]
        points.append(f"<b>Physical Appearance:</b> {t.get('Appearance', '')}")
        points.append(f"<b>General Health:</b> {t.get('Health', '')}")
        points.append(f"<b>Temperament:</b> {t.get('Temperament', '')}")
        points.append(f"<b>Behavioral Traits:</b> {t.get('Behavior', '')}")
        points.append(f"<b>Life Path Focus:</b> {t.get('Life Path', '')}")
        points.append(f"<b>Personality Strength:</b> {t.get('Lord_Traits', '')}")

    # 2. Moon & Emotional Core
    moon_pos = planetary_pos.get('Moon', '')
    m_sign = get_planet_sign(moon_pos)
    points.append(f"<b>Emotional Core:</b> Moon in <b>{m_sign}</b> reflects your inner mind and emotional responsiveness.")
    
    if m_sign in MOON_TRAITS:
        mt = MOON_TRAITS[m_sign]
        points.append(f"<b>Emotional Stability:</b> {mt.get('Emotional Stability', '')}")
        points.append(f"<b>Mindset:</b> {mt.get('Mindset', '')}")
        points.append(f"<b>Emotional Instincts:</b> {mt.get('Instincts', '')}")
        points.append(f"<b>Comfort Zones:</b> Find peace through {mt.get('Comfort Zones', '')}.")
        points.append(f"<b>Moon Dignity:</b> {mt.get('Dignity', '')}")

    # 3. Janma Nakshatra (Vedic Star)
    nak_info = get_nak_info(moon_pos)
    if nak_info:
        nak_name = nak_info['name']
        points.append(f"<b>Janma Nakshatra (Star):</b> You were born under the <b>{nak_name}</b> star (Pada {nak_info['pada']}).")
        if nak_name in NAKSHATRA_TRAITS:
            nt = NAKSHATRA_TRAITS[nak_name]
            points.append(f"<b>Innate Talent:</b> {nt.get('Innate Talent', '')}")
            points.append(f"<b>Karmic Tendency:</b> {nt.get('Karmic Tendency', '')}")
            points.append(f"<b>Behavioral Pattern:</b> {nt.get('Behavioral Pattern', '')}")

    # 4. Sun & Outer Drive
    sun_pos = planetary_pos.get('Sun', '')
    s_sign = get_planet_sign(sun_pos)
    points.append(f"<b>Core Essence:</b> Sun in <b>{s_sign}</b> reflects your outer persona and vital drive.")

    # 5. Potential Indicators (Education & Career)
    if asc_sign in LAGNA_HOUSE_INDICATORS:
        lhi = LAGNA_HOUSE_INDICATORS[asc_sign]
        if "Education" in lhi:
            points.append("<b>Educational Potentials:</b>")
            points.extend(lhi["Education"][:3])
        if "Career" in lhi:
            points.append("<b>Career Potentials:</b>")
            points.extend(lhi["Career"][:3])
        synth = lhi.get("Synthesis", "")
        if synth:
            points.append(f"<b>Life Synthesis:</b> {synth}")

    return {
        "points": list(dict.fromkeys(points))
    }
