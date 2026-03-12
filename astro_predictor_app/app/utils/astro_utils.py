def get_sign_number(sign_name):
    signs = {
        "Aries": 1, "Taurus": 2, "Gemini": 3, "Cancer": 4,
        "Leo": 5, "Virgo": 6, "Libra": 7, "Scorpio": 8,
        "Sagittarius": 9, "Capricorn": 10, "Aquarius": 11, "Pisces": 12
    }
    return signs.get(sign_name, 0)

def get_sign_name(sign_number):
    signs = [
        "", "Aries", "Taurus", "Gemini", "Cancer",
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    if 1 <= sign_number <= 12:
        return signs[sign_number]
    return "Unknown"

def get_planet_sign(position_str):
    if not position_str:
        return ""
    if "(" not in position_str:
        return position_str.strip()
    return position_str.split("(")[0].strip()

def calculate_house(planet_sign, ascendant_sign):
    if not planet_sign or not ascendant_sign:
        return None
    p_num = get_sign_number(planet_sign)
    a_num = get_sign_number(ascendant_sign)
    if p_num == 0 or a_num == 0:
        return None
    house = (p_num - a_num + 1)
    if house <= 0:
        house += 12
    return house

def get_lord(sign_name):
    lords = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
        "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
        "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
    }
    return lords.get(sign_name, "Unknown")

def get_relationship(planet1, planet2):
    friends = {
        "Sun": ["Moon", "Mars", "Jupiter"],
        "Moon": ["Sun", "Mercury"],
        "Mars": ["Sun", "Moon", "Jupiter"],
        "Mercury": ["Sun", "Venus"],
        "Jupiter": ["Sun", "Moon", "Mars"],
        "Venus": ["Mercury", "Saturn"],
        "Saturn": ["Mercury", "Venus"],
        "Rahu": ["Venus", "Saturn", "Mercury"],
        "Ketu": ["Mars", "Sun", "Moon", "Jupiter"]
    }
    enemies = {
        "Sun": ["Venus", "Saturn"],
        "Moon": [],
        "Mars": ["Mercury"],
        "Mercury": ["Moon"],
        "Jupiter": ["Mercury", "Venus"],
        "Venus": ["Sun", "Moon"],
        "Saturn": ["Sun", "Moon", "Mars"],
        "Rahu": ["Sun", "Moon", "Mars"],
        "Ketu": ["Venus", "Saturn", "Mercury"]
    }
    if planet1 == planet2: return "Self"
    if planet2 in friends.get(planet1, []): return "Friend"
    if planet2 in enemies.get(planet1, []): return "Enemy"
    return "Neutral"

def get_ordinal(n):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

def get_house_description(house_num, asc_sign=None):
    descriptions = {
        1: "Self, Personality, Vitality",
        2: "Wealth, Family, Speech",
        3: "Siblings, Courage, Communication",
        4: "Mother, Home, Comforts",
        5: "Children, Intelligence, Creativity",
        6: "Health, Enemies, Debts",
        7: "Spouse, Partners, Business",
        8: "Longevity, Transformation, Occult",
        9: "Luck, Father, Religion",
        10: "Career, Status, Karma",
        11: "Gains, Friends, Wishes",
        12: "Losses, Foreign Lands, Liberation"
    }
    desc = descriptions.get(house_num, "")
    if asc_sign:
        asc_num = get_sign_number(asc_sign)
        if asc_num != 0:
            sign_num = (asc_num + house_num - 1)
            if sign_num > 12: sign_num -= 12
            sign_name = get_sign_name(sign_num)
            return f"{desc} in {sign_name}"
    return desc

def get_dignity(planet_name, sign_name):
    exaltations = {
        "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn",
        "Mercury": "Virgo", "Jupiter": "Cancer", "Venus": "Pisces", "Saturn": "Libra"
    }
    debilitations = {
        "Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer",
        "Mercury": "Pisces", "Jupiter": "Capricorn", "Venus": "Virgo", "Saturn": "Aries"
    }
    if exaltations.get(planet_name) == sign_name:
        return "Exalted"
    if debilitations.get(planet_name) == sign_name:
        return "Debilitated"
    return "Normal"

def get_planet_nature(planet_name):
    """Returns the natural temperament and focus of a planet."""
    natures = {
        "Sun": "authority, leadership, and a desire for visibility",
        "Moon": "emotional intuition, care, and mental flexibility",
        "Mars": "raw energy, competitive drive, and decisive action",
        "Mercury": "analytical precision, effective communication, and logic",
        "Jupiter": "wisdom, expansion, and a focus on growth",
        "Venus": "harmony, artistic flair, and a love for refinements",
        "Saturn": "discipline, long-term structure, and patient endurance",
        "Rahu": "unconventional ambition and a drive for exploration",
        "Ketu": "spiritual depth, detachment, and sudden insights"
    }
    return natures.get(planet_name, "general planetary influence")

def get_house_outcome(house_num, type="pos"):
    """
    Translates house positions/aspects to direct life outcomes for customers.
    """
    outcomes = {
        1: {"pos": "increased vitality, strong self-confidence, and a glowing personality", 
            "neg": "physical exhaustion, self-doubt, or identity shifts"},
        2: {"pos": "steady financial growth and harmonious family relationships", 
            "neg": "fluctuating income or family misunderstandings"},
        3: {"pos": "bold communication and successful short-distance ventures", 
            "neg": "miscommunications or lack of courage in new efforts"},
        4: {"pos": "peaceful domestic life, happiness at home, and property gains", 
            "neg": "domestic stress or delays in property matters"},
        5: {"pos": "creative breakthroughs, success in studies, and joy through children", 
            "neg": "mental blocks, speculative losses, or concerns for children"},
        6: {"pos": "victory over challenges and excellent daily work productivity", 
            "neg": "health hurdles, increased workload, or competition from rivals"},
        7: {"pos": "smooth partnerships, marital bliss, and successful public dealings", 
            "neg": "frictions in partnerships or misunderstandings with spouse"},
        8: {"pos": "unexpected gains, deep transformation, and sudden positive shifts", 
            "neg": "unexpected setbacks, sudden changes, or health anxieties"},
        9: {"pos": "steady luck, successful higher learning, and spiritual growth", 
            "neg": "delays in travel, father-related concerns, or blocked fortune"},
        10: {"pos": "elevated career status, public recognition, and success in work", 
             "neg": "professional hurdles, stress at workplace, or status instability"},
        11: {"pos": "fulfilment of long-held desires and major financial profits", 
             "neg": "delayed gains or disappointments in social networks"},
        12: {"pos": "successful foreign connections and deep spiritual peace", 
             "neg": "unexpected expenses or feelings of isolation"}
    }
    return outcomes.get(house_num, {}).get(type, "general life changes")

def is_retrograde(position_str):
    return "(R)" in position_str

def get_ruled_houses(planet, ascendant_sign):
    """Returns the house numbers ruled by the given planet."""
    if planet in ["Rahu", "Ketu", "None", "Unknown"]:
        return []
    
    lord_map = {
        "Sun": ["Leo"],
        "Moon": ["Cancer"],
        "Mars": ["Aries", "Scorpio"],
        "Mercury": ["Gemini", "Virgo"],
        "Jupiter": ["Sagittarius", "Pisces"],
        "Venus": ["Taurus", "Libra"],
        "Saturn": ["Capricorn", "Aquarius"]
    }
    
    ruled_signs = lord_map.get(planet, [])
    houses = []
    for sign in ruled_signs:
        h = calculate_house(sign, ascendant_sign)
        if h: houses.append(h)
    return houses

def get_aspects(planet, p_sign, asc_sign):
    """Calculates house numbers aspected by a planet."""
    if not p_sign or not asc_sign: return []
    p_house = calculate_house(p_sign, asc_sign)
    if not p_house: return []
    
    # All planets aspect the 7th from their position
    aspects = [(p_house + 7 - 1) % 12 + 1]
    
    # Special aspects
    if planet == "Mars":
        aspects.extend([(p_house + 4 - 1) % 12 + 1, (p_house + 8 - 1) % 12 + 1])
    elif planet == "Jupiter" or planet == "Rahu" or planet == "Ketu":
        aspects.extend([(p_house + 5 - 1) % 12 + 1, (p_house + 9 - 1) % 12 + 1])
    elif planet == "Saturn":
        aspects.extend([(p_house + 3 - 1) % 12 + 1, (p_house + 10 - 1) % 12 + 1])
        
    return sorted(list(set(aspects)))

def analyze_planetary_aspects(planetary_pos, asc_sign, target_houses):
    observations = []
    for planet, pos_str in planetary_pos.items():
        if planet == 'Mandhi': continue
        p_sign = get_planet_sign(pos_str)
        p_house = calculate_house(p_sign, asc_sign)
        if not p_house: continue
        if p_house in target_houses:
            outcome = get_house_outcome(p_house, type='pos' if planet in ['Jupiter', 'Venus', 'Mercury', 'Moon'] else 'neg')
            observations.append(f"<b>Influence on {get_ordinal(p_house)} House:</b> {planet}'s presence directly triggers **{outcome}**.")
        aspects = get_aspects(planet, p_sign, asc_sign)
        for ah in aspects:
            if ah in target_houses:
                outcome = get_house_outcome(ah, type='pos' if planet in ['Jupiter', 'Venus'] else 'neg')
                observations.append(f"<b>Notice:</b> {planet} influences your {get_ordinal(ah)} house, leading to **{outcome}**.")
    return observations

def analyze_transits(transit_pos, asc_sign, target_houses):
    observations = []
    for planet in ["Jupiter", "Saturn", "Rahu", "Ketu"]:
        t_pos = transit_pos.get(planet)
        if not t_pos: continue
        t_sign = get_planet_sign(t_pos)
        t_house = calculate_house(t_sign, asc_sign)
        if not t_house: continue
        if t_house in target_houses:
            outcome = get_house_outcome(t_house, type='pos' if planet == 'Jupiter' else 'neg')
            observations.append(f"<b>Current Transit:</b> Moving {planet} is currently activating **{outcome}**.")
    return observations

def analyze_jamakkol(jamakkol_data, asc_sign, category_houses):
    observations = []
    if not jamakkol_data: return []
    udayam = jamakkol_data.get('Udayam')
    arudham = jamakkol_data.get('Arudham')
    kavippu = jamakkol_data.get('Kavippu')
    if udayam:
        u_house = calculate_house(udayam, asc_sign)
        if u_house in category_houses:
             observations.append(f"<b>Immediate Focus:</b> Current energy is high for **{get_house_outcome(u_house)}**. Action taken now will bring results.")
    if arudham:
        a_house = calculate_house(arudham, asc_sign)
        if a_house in category_houses:
             observations.append(f"<b>Outcome Hint:</b> Indicators suggest a favorable path regarding **{get_house_outcome(a_house, type='pos')}**.")
    if kavippu:
        k_house = calculate_house(kavippu, asc_sign)
        if k_house in category_houses:
             observations.append(f"<b>Caution:</b> Temporary hurdles are present in **{get_house_outcome(k_house, type='neg')}**. Patience is advised.")
    return observations

def analyze_dasa_bhukti_detailed(dasa_info, key_lords_map, category_name="General"):
    """
    Analyzes the current Dasa/Bhukti/Antara lords with category-specific implications.
    """
    observations = []
    if not dasa_info: return []
    
    d_lord = dasa_info.get('dasa', {}).get('lord')
    b_lord = dasa_info.get('bhukti', {}).get('lord')
    
    if d_lord:
        observations.append(f"<b>Mahadasa (Main Age Period):</b> You are in the major cycle of {d_lord}. This planet sets the long-term theme for your {category_name.lower()} trajectory.")
    if b_lord:
        # Context-rich sub-period explanation
        focus = "patience and structural stability" if b_lord == "Saturn" else \
                "unconventional growth and sudden shifts" if b_lord == "Rahu" else \
                "expansion and wisdom" if b_lord == "Jupiter" else \
                "harmony and material gains" if b_lord == "Venus" else \
                "logic and communication" if b_lord == "Mercury" else \
                "raw energy and initiative" if b_lord == "Mars" else \
                "mental adaptability" if b_lord == "Moon" else \
                "authority and visibility" if b_lord == "Sun" else \
                "detachment and spiritual insights"
        observations.append(f"<b>Bhukti (Current Sub-Cycle):</b> The {b_lord} sub-period is active, bringing a focus on **{focus}** to your {category_name.lower()} matters.")
        
    return observations
