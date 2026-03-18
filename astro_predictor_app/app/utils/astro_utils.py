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

def get_nak_info(pos_str):
    if not pos_str or not isinstance(pos_str, (str, dict)):
        return None
    try:
        # Handle dict or string
        if isinstance(pos_str, dict):
            return {"name": pos_str.get("nakshatra"), "pada": pos_str.get("pada")}
            
        # Format: "Sign (Deg° Min')"
        if " (" not in pos_str: return None
        sign_part = pos_str.split(" (")[0]
        deg_part = pos_str.split(" (")[1].split("°")[0]
        min_part = pos_str.split("° ")[1].split("'")[0]
        
        sign_base_deg = (get_sign_number(sign_part) - 1) * 30
        total_deg = sign_base_deg + float(deg_part) + float(min_part)/60.0
        
        nak_names = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
            "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
            "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]
        
        nak_idx = int(total_deg // (360/27))
        nak_name = nak_names[nak_idx]
        pada = int((total_deg % (360/27)) // (360/108)) + 1
        return {"name": nak_name, "pada": pada}
    except:
        return None

def get_planet_sign(position):
    if isinstance(position, dict):
        return position.get('sign', '')
    if not position or not isinstance(position, str):
        return ""
    if "(" not in position:
        return position.strip()
    return position.split("(")[0].strip()

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

def get_house_outcome(house_num, type="pos", category="Career"):
    """
    Translates house positions/aspects to direct life outcomes for customers, 
    contextualized by category (Health, Education, Career, etc.).
    """
    # Shared outcomes mapping
    outcomes = {
        "Career": {
            1: {"pos": "increased vitality, strong self-confidence, and a glowing personality", "neg": "physical exhaustion, self-doubt, or identity shifts"},
            2: {"pos": "steady financial growth and harmonious family relationships", "neg": "fluctuating income or family misunderstandings"},
            3: {"pos": "bold communication and successful short-distance ventures", "neg": "miscommunications or lack of courage in new efforts"},
            4: {"pos": "peaceful domestic life, happiness at home, and property gains", "neg": "domestic stress or delays in property matters"},
            5: {"pos": "creative breakthroughs, success in studies, and joy through children", "neg": "mental blocks, speculative losses, or concerns for children"},
            6: {"pos": "victory over challenges and excellent daily work productivity", "neg": "health hurdles, increased workload, or competition from rivals"},
            7: {"pos": "smooth partnerships, marital bliss, and successful public dealings", "neg": "frictions in partnerships or misunderstandings with spouse"},
            8: {"pos": "unexpected gains, deep transformation, and sudden positive shifts", "neg": "unexpected setbacks, sudden changes, or health anxieties"},
            9: {"pos": "steady luck, successful higher learning, and spiritual growth", "neg": "delays in travel, father-related concerns, or blocked fortune"},
            10: {"pos": "elevated career status, public recognition, and success in work", "neg": "professional hurdles, stress at workplace, or status instability"},
            11: {"pos": "fulfilment of long-held desires and major financial profits", "neg": "delayed gains or disappointments in social networks"},
            12: {"pos": "successful foreign connections and deep spiritual peace", "neg": "unexpected expenses or feelings of isolation"}
        },
        "Health": {
            1: {"pos": "strong immunity, high physical energy, and robust vitality", "neg": "physical fatigue, self-doubt, or low stamina"},
            2: {"pos": "healthy habits, facial glow, and overall family well-being", "neg": "dietary imbalances or minor speech/throat issues"},
            3: {"pos": "energetic movement, strong respiratory health, and physical courage", "neg": "nervous tension or minor respiratory concerns"},
            4: {"pos": "mental peace, emotional stability, and heart health", "neg": "emotional stress, chest congestion, or home-related anxiety"},
            5: {"pos": "healthy digestion, strong creative energy, and mental clarity", "neg": "stomach sensitivity or mental fatigue"},
            6: {"pos": "victory over illness, strong digestive fire, and resilience", "neg": "health hurdles, susceptibility to seasonal illness, or fatigue"},
            7: {"pos": "balanced physical relations and harmonious social health", "neg": "partner-related stress or lower back sensitivity"},
            8: {"pos": "strong restorative powers, longevity, and deep internal healing", "neg": "unexpected health changes, sudden fatigue, or chronic worries"},
            9: {"pos": "positive physiological growth, luck in recovery, and spiritual health", "neg": "hip/thigh sensitivity or delays in healing"},
            10: {"pos": "strong kneecap health, active lifestyle, and public vitality", "neg": "joint stiffness, professional stress impacting health, or fatigue"},
            11: {"pos": "strong limb vitality, fulfillment of health goals, and social well-being", "neg": "circulatory issues or delays in health improvements"},
            12: {"pos": "peaceful sleep, successful hospitalization if needed, and spiritual release", "neg": "insomnia, unexpected medical expenses, or isolation"}
        },
        "Education": {
            1: {"pos": "increased mental focus, academic confidence, and self-belief", "neg": "academic fatigue, self-doubt, or focus shifts"},
            2: {"pos": "strong foundational learning, good memory, and effective speech", "neg": "difficulties in basic memorization or early learning delays"},
            3: {"pos": "bold expression in studies and success in skill-based learning", "neg": "misunderstanding instructions or lack of interest in practicals"},
            4: {"pos": "peaceful study environment at home and foundational schooling success", "neg": "distractions at home or delays in completing schooling"},
            5: {"pos": "creative breakthroughs in projects and excellent intelligence", "neg": "concentration blocks or delays in competitive exams"},
            6: {"pos": "victory in academic competitions and disciplined study routines", "neg": "learning hurdles, peer competition, or exam stress"},
            7: {"pos": "successful group projects and learning through social partners", "neg": "social distractions or misunderstandings in collaborative work"},
            8: {"pos": "deep research skills, success in occult or technical studies", "neg": "unexpected shifts in subjects or sudden academic delays"},
            9: {"pos": "luck in higher education and success in foreign certifications", "neg": "delays in university admissions or blocked higher learning"},
            10: {"pos": "public recognition for studies and authority in your subject", "neg": "pressure from authority figures or academic status concerns"},
            11: {"pos": "fulfilment of academic goals and gains through study networks", "neg": "delayed results or disappointments in academic clubs"},
            12: {"pos": "success in overseas education and deep technical research", "neg": "unexpected study expenses or feelings of academic isolation"}
        },
        "Finance": {
            1: {"pos": "personality that attracts wealth and professional status", "neg": "personal expenses impacting savings"},
            2: {"pos": "steady accumulation of wealth and family prosperity", "neg": "fluctuating income or family-related expenses"},
            3: {"pos": "gains through initiatives, travel, and communication", "neg": "unproductive expenses on short trips"},
            4: {"pos": "gains through property, vehicles, and domestic comforts", "neg": "expenditure on home repairs or property delays"},
            5: {"pos": "profits through investments, speculation, and creativity", "neg": "speculative losses or fluctuating returns"},
            6: {"pos": "success in recovering debts and gains through service", "neg": "increased debts or hidden financial hurdles"},
            7: {"pos": "financial gains through partnerships and business ventures", "neg": "partnership-related losses or legal expenses"},
            8: {"pos": "unexpected inheritance, insurance gains, or sudden wealth", "neg": "unexpected financial setbacks or sudden large expenses"},
            9: {"pos": "long-term fortune, gains through distant lands or Father", "neg": "blocked fortune or delays in financial luck"},
            10: {"pos": "wealth through professional status and career success", "neg": "status-related expenses or workplace financial stress"},
            11: {"pos": "multiple streams of income and fulfillment of financial wishes", "neg": "delayed profits or disappointment in expected gains"},
            12: {"pos": "gains through foreign trade and spiritual ventures", "neg": "wasteful expenditure or heavy foreign-related outflows"}
        },
        "Relationships": {
            1: {"pos": "charming personality and positive social interactions", "neg": "self-centeredness impacting bonds"},
            2: {"pos": "harmonious family life and sweet-spoken nature", "neg": "family misunderstandings or harsh speech"},
            3: {"pos": "strong bonding with siblings and neighbors", "neg": "misunderstandings with close associates"},
            4: {"pos": "deep emotional happiness and peace at home", "neg": "domestic tensions or lack of emotional comfort"},
            5: {"pos": "joy through romantic interests and creative bonds", "neg": "misunderstandings in romance or mental worry"},
            6: {"pos": "ability to overcome relationship challenges", "neg": "conflicts with colleagues or minor frictions"},
            7: {"pos": "strong marital bliss and successful partnerships", "neg": "frictions in marriage or partnership delays"},
            8: {"pos": "deep transformative bonds and shared intensity", "neg": "sudden shifts in relationships or occult-related stress"},
            9: {"pos": "growth of relationships through shared wisdom and travel", "neg": "difference of opinion in philosophical matters"},
            10: {"pos": "public recognition for bond and status in society", "neg": "professional life impacting personal relationships"},
            11: {"pos": "support from friends and fulfillment of social bonds", "neg": "disappointments in social circles or delayed support"},
            12: {"pos": "peaceful solitude or spiritual connection in bonds", "neg": "feelings of isolation or foreign-related separations"}
        },
        "Children": {
            1: {"pos": "increased focus on children and parental identity", "neg": "personal stress impacting parental duties"},
            2: {"pos": "family growth and happiness through offspring", "neg": "concerns regarding child's early habits"},
            3: {"pos": "child's initiative and courage in activities", "neg": "minor disagreements with older children"},
            4: {"pos": "domestic joy and emotional comfort through children", "neg": "child-related home disruptions"},
            5: {"pos": "bright future for children and strong bonding", "neg": "health concerns or study blocks for children"},
            6: {"pos": "child's victory over challenges and disciplined life", "neg": "child-related hurdles or minor health issues"},
            7: {"pos": "social recognition for children and good partnerships", "neg": "concerns about child's social associations"},
            8: {"pos": "sudden positive shifts in child's life direction", "neg": "sudden changes or unexpected concerns for children"},
            9: {"pos": "spiritual growth for children and higher learning success", "neg": "delays in child's higher development"},
            10: {"pos": "status and recognition through child's achievements", "neg": "status-related pressure on children"},
            11: {"pos": "fulfillment of hopes regarding children and prosperity", "neg": "delayed milestones or disappointment in gains"},
            12: {"pos": "child's success in foreign lands or spiritual depth", "neg": "child-related expenses or foreign separations"}
        },
        "Business": {
            1: {"pos": "strong entrepreneurial drive and personal brand growth", "neg": "personal identity conflicts impacting business"},
            2: {"pos": "steady commercial growth and wealth accumulation", "neg": "fluctuating business income or cash flow blocks"},
            3: {"pos": "success in marketing, trade, and communication", "neg": "misunderstandings in contracts or trade delays"},
            4: {"pos": "stable business foundations and property gains", "neg": "domestic distractions impacting business focus"},
            5: {"pos": "creative breakthroughs in products and speculative gains", "neg": "intellectual blocks or investment setbacks"},
            6: {"pos": "victory over competitors and disciplined service", "neg": "employee-related hurdles or business debt stress"},
            7: {"pos": "successful partnerships and expanding client base", "neg": "frictions in partnerships or legal delays"},
            8: {"pos": "sudden transformative gains or research success", "neg": "unexpected market shifts or hidden business hurdles"},
            9: {"pos": "global expansion and success in distant markets", "neg": "blocked business luck or delays in foreign trade"},
            10: {"pos": "authority in your industry and public recognition", "neg": "pressure from authorities or status-related stress"},
            11: {"pos": "fulfillment of business goals and massive gains", "neg": "delayed profits or disappointment in networks"},
            12: {"pos": "success in export-import or foreign ventures", "neg": "unproductive business expenses or foreign setbacks"}
        },
        "Legal": {
            1: {"pos": "strong personal stance and legal confidence", "neg": "personal stress impacting legal focus"},
            2: {"pos": "successful family-related legal settlements", "neg": "family disputes over assets or harsh speech"},
            3: {"pos": "victory through bold initiatives and documents", "neg": "misunderstandings in legal paperwork"},
            4: {"pos": "favorable property-related legal outcomes", "neg": "domestic-related legal hurdles"},
            5: {"pos": "creative wins and success in high-stakes cases", "neg": "intellectual blocks in legal strategy"},
            6: {"pos": "victory over litigation and disciplined defense", "neg": "ongoing legal battles or opponent pressure"},
            7: {"pos": "successful out-of-court settlements", "neg": "frictions in legal partnerships or opponent strength"},
            8: {"pos": "sudden positive shifts in complex cases", "neg": "sudden legal setbacks or hidden court hurdles"},
            9: {"pos": "judgement in your favor and higher court success", "neg": "blocked luck in legal matters or delays"},
            10: {"pos": "recognition for fair stance and authority win", "neg": "status-related legal pressure or authority hurdles"},
            11: {"pos": "final settlement gains and wish fulfillment", "neg": "delayed legal gains or disappointment in results"},
            12: {"pos": "success in foreign-related legal matters", "neg": "legal expenses or foreign court hurdles"}
        },
        "Spirituality": {
            1: {"pos": "strong soul connection and inner peace", "neg": "ego issues impacting spiritual growth"},
            2: {"pos": "sacred speech and harmonious inner values", "neg": "worldly attachments impacting values"},
            3: {"pos": "boldness in spiritual practices and travel", "neg": "misunderstandings in spiritual teachings"},
            4: {"pos": "deep emotional peace and sanctuary at home", "neg": "domestic distractions from meditation"},
            5: {"pos": "creative inspiration and divine grace", "neg": "mental wavering or blocks in devotion"},
            6: {"pos": "victory over inner enemies (lust, anger, etc.)", "neg": "health blocks in practice or peer conflict"},
            7: {"pos": "spiritual partnerships and shared growth", "neg": "frictions in spiritual associations"},
            8: {"pos": "deep mystical insights and transformative growth", "neg": "sudden shifts or hidden spiritual hurdles"},
            9: {"pos": "luck in finding a Guru and higher wisdom", "neg": "blocked fortune in spiritual path"},
            10: {"pos": "authority in spiritual field and recognition", "neg": "status concerns impacting humble growth"},
            11: {"pos": "fulfillment of spiritual hopes and gains", "neg": "delayed realizations or social blocks"},
            12: {"pos": "perfect solitude and connection with the Divine", "neg": "isolation stress or foreign-related blocks"}
        },
        "Travel": {
            1: {"pos": "strong desire for travel and personal exploration", "neg": "travel-related personal stress or identity shifts"},
            2: {"pos": "gains through family travel or foreign resources", "neg": "expenses related to travel or family separations"},
            3: {"pos": "success in short trips, Skill-based travel, and trade", "neg": "misunderstandings during travel or short trip delays"},
            4: {"pos": "comfort in foreign lands or gain through foreign property", "neg": "feelings of homesickness or domestic-related travel blocks"},
            5: {"pos": "joyful travel for recreation or creative learning", "neg": "concerns regarding child's travel or speculative losses abroad"},
            6: {"pos": "victory over travel-related hurdles and disciplined trips", "neg": "health issues during travel or legal hurdles abroad"},
            7: {"pos": "successful foreign partnerships and business travel", "neg": "frictions in foreign associations or partnership delays"},
            8: {"pos": "sudden transformative foreign experiences", "neg": "unexpected travel setbacks or sudden foreign hurdles"},
            9: {"pos": "luck in long-distance travel and pilgrimage success", "neg": "blocked fortune in distant lands or visa delays"},
            10: {"pos": "professional recognition in foreign lands and status", "neg": "status-related pressure abroad or authority hurdles"},
            11: {"pos": "fulfillment of travel goals and massive foreign gains", "neg": "delayed foreign profits or disappointment in networks abroad"},
            12: {"pos": "success in permanent foreign settlement and peace", "neg": "isolation in foreign lands or unexpected foreign expenses"}
        },
        "Property": {
            1: {"pos": "personal focus on asset building and home comfort", "neg": "property-related personal stress or delays"},
            2: {"pos": "steady accumulation of fixed assets and family property", "neg": "family disputes over land or wealth blocks"},
            3: {"pos": "success in property deals, documents, and short-trip visits", "neg": "legal hurdles in property paperwork or trade delays"},
            4: {"pos": "massive gains through ancestral land and domestic peace", "neg": "domestic hurdles or repair issues in main residence"},
            5: {"pos": "speculative gains through land or creative home design", "neg": "intellectual blocks in property choice or investment loss"},
            6: {"pos": "victory in land disputes and successful property service", "neg": "property-related litigation or maintenance debt"},
            7: {"pos": "successful property partnerships and fair deals", "neg": "frictions in land associations or agreement delays"},
            8: {"pos": "sudden transformative asset gains or hidden property discovery", "neg": "unexpected damage to property or sudden land hurdles"},
            9: {"pos": "luck in distant property investments and religious land", "neg": "blocked fortune in long-distance property or visa/legal delays"},
            10: {"pos": "professional status through real estate and authority", "neg": "status-related pressure or authority hurdles in land"},
            11: {"pos": "fulfillment of property goals and massive capital gains", "neg": "delayed asset profits or disappointment in property networks"},
            12: {"pos": "success in foreign real estate or peaceful isolated home", "neg": "unexpected expenses on land or foreign property setbacks"}
        }
    }
    
    # Fallback to Career if category not found, then to General
    cat_data = outcomes.get(category, outcomes["Career"])
    return cat_data.get(house_num, {}).get(type, "general life changes")

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

def get_dynamic_recommendations(planetary_pos, asc_sign, category):
    """
    Calculates dynamic recommendations based on planetary strengths and house placements.
    """
    category_map = {
        'Education': {
            'Mercury': ["IT & Computer Science", "Media & Journalism", "Mathematics & Statistics", "Commerce & Trade"],
            'Jupiter': ["Law & Legal Studies", "Teaching & Philosophy", "Finance & Banking", "Sanskrit & Mythology"],
            'Sun': ["Political Science", "Government Administration", "Medical Sciences", "Leadership Studies"],
            'Mars': ["Mechanical Engineering", "Civil Engineering", "Sports Sciences", "Military Arts"],
            'Venus': ["Fine Arts & Design", "Fashion & Interior Design", "Hospitality Management", "Performing Arts"],
            'Saturn': ["Architecture", "History & Archaeology", "Social Work", "Structural Engineering"],
            'Moon': ["Psychology & Nursing", "Creative Arts", "Hospitality Management", "Public Relations"],
            'Rahu': ["Innovation & Technology", "Specialized Research", "Foreign Languages", "Digital Arts"],
            'Ketu': ["Occult Sciences", "Deep Research", "Mathematics", "Spirtual Studies"]
        },
        'Finance': {
            'Jupiter': ["Banking & Financial Services", "Investment & Asset Growth", "Advisory", "Precious Metals"],
            'Venus': ["Luxury Retail & Arts", "Hospitality & Tourism", "Fashion Business", "Vehicle Industry"],
            'Mercury': ["Trading & Stocks", "E-commerce", "Accounting & Audit", "Communication Services"],
            'Moon': ["Dairy & Food Industry", "Import-Export", "Psychology & Nurturing", "Silver & Pearls"],
            'Sun': ["Government Contracts", "Public Sector Projects", "Leadership Roles", "Inheritance"],
            'Mars': ["Real Estate & Construction", "Mining & Metals", "Agricultural Business", "Security Sector"],
            'Saturn': ["Infrastructure", "Traditional Manufacturing", "Mining", "Slow-growth Assets"],
            'Rahu': ["Foreign Investments", "Digital Innovation", "Cryptocurrency", "High-risk Speculation"],
            'Ketu': ["Inheritance", "Occult Research Services", "Detached Consultation", "Hidden Assets"]
        },
        'Health': {
             'Sun': ["Vitality & Heart Strength", "Bone Health", "Eyes & Vision"],
             'Moon': ["Emotional Balance", "Fluid Levels", "Digestive Rhythm", "Chest Health"],
             'Mars': ["Physical Energy", "Blood & Muscle Strength", "Marrow Health"],
             'Mercury': ["Nervous System", "Skin Health", "Communication Clarity", "Shoulder Strength"],
             'Jupiter': ["Liver Health", "Growth & Immunity", "Ear Health"],
             'Venus': ["Reproductive Balance", "Throat & Neck", "Skin Glow"],
             'Saturn': ["Bone Structure & Joints", "Longevity", "Teeth & Hair"],
             'Rahu': ["Immune System Sensitivity", "Phobias & Mental Tension", "Unusual Sensitivities"],
             'Ketu': ["Spiritual Clarity", "Genetic Health", "Healing Recovery"]
        },
        'Relationships': {
             'Venus': ["Harmony & Romance", "Artistic Bond", "Beauty & Comfort"],
             'Jupiter': ["Wisdom & Growth", "Traditional Values", "Spiritual Connection"],
             'Mars': ["Passion & Energy", "Dynamic Partnership", "Bold Initiatives"],
             'Moon': ["Emotional Nurturing", "Deep Intuition", "Home Family Focus"],
             'Mercury': ["Communication & Wit", "Intellectual Sharing", "Travel Together"],
             'Sun': ["Loyalty & Status", "Leadership Balance", "Mutual Respect"],
             'Saturn': ["Stability & Endurance", "Grounded Reality", "Long-term Duty"],
             'Rahu': ["Unconventional Dynamic", "Innovation Together", "Foreign Connections"],
             'Ketu': ["Spiritual Depth", "Detachment & Healing", "Past Life Connection"]
        },
        'Children': {
             'Jupiter': ["Joy through Progeny", "Success of Children", "Traditional Values"],
             'Moon': ["Nurturing Connection", "Strong Emotional Bond", "Caring Nature"],
             'Mercury': ["Intellectual Growth", "Active Communication", "Creative Hobbies"],
             'Venus': ["Artistic Talents", "Happiness & Comfort", "Pleasant Relationship"],
             'Sun': ["Leadership Potential", "Respect & Status", "Legacy Focus"],
             'Mars': ["High Energy", "Competitive Spirit", "Independent Nature"],
             'Saturn': ["Disciplined Growth", "Long-term Responsibility", "Steady Progress"],
             'Rahu': ["Unconventional Talents", "Modern Innovation", "Multi-faceted Potential"],
             'Ketu': ["Spiritual Intuition", "Unique Research Skills", "Detached Wisdom"]
        },
        'Property': {
             'Mars': ["Land & Real Estate", "Construction Projects", "Agricultural Land"],
             'Venus': ["Luxury Homes & Villas", "Interior Design Focus", "Cosmetic Renovations"],
             'Saturn': ["Old Property & Ancestral Home", "Structural Stability", "Long-term Assets"],
             'Jupiter': ["Spacious Assets", "Legal Regularization", "Lucky Acquisitions"],
             'Sun': ["Government Property", "Prestigious Location", "Inherited Status"],
             'Moon': ["Residential Plots", "Water-side Property", "Farmhouses"],
             'Mercury': ["Commercial Property", "Shared/Rental Assets", "Plots for Development"]
        },
        'Business': {
             'Mercury': ["Trading & E-commerce", "Consultancy Services", "Agency & Distribution"],
             'Sun': ["Independent Leadership", "Corporate Contracts", "Brand Management"],
             'Mars': ["Manufacturing & Construction", "Risk-taking Ventures", "Energy & Security"],
             'Rahu': ["Digital Innovation", "Import-Export", "Unconventional Niche"],
             'Saturn': ["Traditional Industry", "Labor-intensive Business", "Mining & Metals"],
             'Jupiter': ["Financial Services", "Training & Education Sector", "Legal Advisory"],
             'Venus': ["Artistic Ventures", "Luxury Retail", "Entertainment Business"],
             'Moon': ["Food & Beverage", "Import-Export of Liquids", "Nurturing Services"]
        },
        'Travel': {
             'Moon': ["Short Pleasure Trips", "Water-side Destinations", "Frequent Changes"],
             'Venus': ["Luxury & Leisure Travel", "Cultural Explorations", "Artistic Destinations"],
             'Rahu': ["Foreign/International Travel", "Technological Shifts", "Dynamic New Environments"],
             'Jupiter': ["Spiritual Pilgrimages", "Higher Learning Travel", "Wise Exploration"],
             'Saturn': ["Distant & Necessary Travel", "Delayed but Stable Stays", "Working Abroad"],
             'Sun': ["Official/Government Travel", "Status-enhancing Voyages"],
             'Mars': ["Adventure & Sports Travel", "Quick Business Trips"]
        },
        'Legal': {
             'Jupiter': ["Legal Advisory & Counsel", "Success in Litigation", "Ethical Resolution"],
             'Saturn': ["Disciplinary Proceedings", "Patience in Settlements", "Strict Law Compliance"],
             'Sun': ["Government Regulations", "Public Policy Matters", "Authoritative Judgments"],
             'Mars': ["Dispute Management", "Competitive Legal Action", "Direct Negotiations"],
             'Mercury': ["Drafting & Documentation", "IP & Trade Law", "Legal Communication"]
        },
        'Spirituality': {
             'Jupiter': ["Vedic Wisdom & Philosophy", "Spiritual Guru Guidance", "Religious Studies"],
             'Ketu': ["Moksha & Liberation Research", "Deep Meditation", "Healing & Detachment"],
             'Sun': ["Self-Realization Path", "Leadership in Charity", "Soulful Awareness"],
             'Moon': ["Emotional Healing", "Intuitive Connection", "Bhakti & Devotion"],
             'Saturn': ["Disciplined Penance", "Traditional Rituals", "Solitary Service"],
             'Rahu': ["Unconventional Paths", "Technical Spirituality", "Global Wisdom"]
        },
        'Vehicles': {
             'Venus': ["Luxury & Stylish Vehicles", "Comfortable Travel", "Artistic Design Focus"],
             'Mars': ["Performance & Speed", "Technical & Mechanical Excellence", "Daring Commutes"],
             'Moon': ["Smooth & Fluid Motion", "Family Convenience", "Short Pleasant Drives"],
             'Saturn': ["Durable & Traditional Vehicles", "Utility-focused Transport", "Heavy/Old Models"],
             'Mercury': ["Compact & Practical Cars", "Communication-equipped Transport", "City Commuters"]
        },
        'Career': {
             'Sun': ["Government & Administration", "Leadership & Management", "Public Recognition", "Authority Roles"],
             'Moon': ["Public Relations", "Hospitality & Nurturing", "Psychology & Counseling", "Creative Arts"],
             'Mars': ["Engineering & Technology", "Security & Defense", "Surgery & Medical", "Construction & Real Estate"],
             'Mercury': ["Accounts & Auditing", "Media & Communication", "IT & Software", "Trade & Commerce"],
             'Jupiter': ["Finance & Banking", "Teaching & Training", "Legal & Judiciary", "Advisory & Consulting"],
             'Venus': ["Arts & Entertainment", "Luxury & Fashion", "Design & Architecture", "Hospitality"],
             'Saturn': ["Infrastructure & Labor", "Traditional Industry", "Mining & Metals", "Service & Discipline"],
             'Rahu': ["Innovation & Research", "Foreign Connections", "Digital Media", "Technical Specialization"],
             'Ketu': ["Spiritual Guidance", "Deep Research", "Occult Sciences", "Healing & Therapy"]
        }
    }

    if category not in category_map:
        return []

    planet_map = category_map[category]
    scores = {p: 0 for p in planet_map.keys()}
    
    # Target houses vary by category
    house_weights = {
        'Education': {4: 40, 5: 30, 2: 15, 9: 15, 1: 10},
        'Finance': {2: 40, 11: 30, 5: 15, 9: 15, 1: 10},
        'Health': {1: 40, 6: -20, 8: 15, 5: 10},
        'Relationships': {7: 40, 1: 20, 5: 15, 11: 15, 2: 10},
        'Children': {5: 40, 9: 20, 11: 20, 1: 10, 2: 10},
        'Property': {4: 40, 2: 20, 11: 20, 10: 10},
        'Business': {10: 40, 7: 20, 11: 20, 2: 10},
        'Travel': {9: 40, 12: 30, 3: 20, 7: 10},
        'Legal': {9: 30, 10: 30, 6: 20, 12: 10},
        'Spirituality': {9: 40, 12: 30, 5: 20, 1: 10},
        'Vehicles': {4: 40, 2: 20, 11: 20, 1: 10}
    }.get(category, {10: 40, 11: 20, 1: 15, 2: 15})

    for planet, roles in planet_map.items():
        p_pos = planetary_pos.get(planet, '')
        if not p_pos: continue
        
        p_sign = get_planet_sign(p_pos)
        p_house = calculate_house(p_sign, asc_sign)
        p_dig = get_dignity(planet, p_sign)
        
        # 1. House Placement
        weight = house_weights.get(p_house, 0)
        scores[planet] += weight
        
        # 2. Dignity
        if 'Exalted' in p_dig or 'Own' in p_dig: scores[planet] += 30
        elif 'Friend' in p_dig: scores[planet] += 15
        elif 'Debilitated' in p_dig: scores[planet] -= 20
        
        # Cross-category specific logic
        if category == 'Health' and p_house == 6:
             scores[planet] -= 30 # Malefics in 6 are good for victory but planets in 6 point to vulnerabilities

    # Identify Top 2 Planets
    sorted_planets = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    recs = []
    count = 0
    for p, score in sorted_planets:
        if count >= 2: break
        if score >= 10:
             recs.extend(planet_map[p][:2])
             count += 1
             
    return list(dict.fromkeys(recs))

def analyze_planetary_combinations(planetary_pos, asc_sign, target_houses, category="Career"):
    """Identifies and analyzes planetary conjunctions in target houses."""
    conjunctions = {}
    for planet, pos in planetary_pos.items():
        if planet == 'Mandhi': continue
        p_sign = get_planet_sign(pos)
        p_house = calculate_house(p_sign, asc_sign)
        if p_house in target_houses:
            if p_house not in conjunctions: conjunctions[p_house] = []
            conjunctions[p_house].append(planet)
            
    observations = []
    for house, planets in conjunctions.items():
        if len(planets) > 1:
            planet_list = " and ".join(planets) if len(planets) == 2 else ", ".join(planets[:-1]) + ", and " + planets[-1]
            natures = " combined with ".join([get_planet_nature(p) for p in planets])
            outcome = get_house_outcome(house, category=category)
            observations.append(f"<b>Planetary Combination:</b> {planet_list} are together in your {get_ordinal(house)} house. This creates a powerful synergy of {natures}, focusing intensely on <b>{outcome}</b>.")
    return observations

def analyze_planetary_aspects(planetary_pos, asc_sign, target_houses, category="Career"):
    observations = []
    for planet, pos_str in planetary_pos.items():
        if planet == 'Mandhi': continue
        p_sign = get_planet_sign(pos_str)
        p_house = calculate_house(p_sign, asc_sign)
        if not p_house: continue
        if p_house in target_houses:
            outcome = get_house_outcome(p_house, type='pos' if planet in ['Jupiter', 'Venus', 'Mercury', 'Moon'] else 'neg', category=category)
            observations.append(f"<b>Influence on {get_ordinal(p_house)} House:</b> {planet}'s presence directly triggers <b>{outcome}</b>.")
        aspects = get_aspects(planet, p_sign, asc_sign)
        for ah in aspects:
            if ah in target_houses:
                outcome = get_house_outcome(ah, type='pos' if planet in ['Jupiter', 'Venus'] else 'neg', category=category)
                observations.append(f"<b>Notice:</b> {planet} influences your {get_ordinal(ah)} house, leading to <b>{outcome}</b>.")
    return observations

def analyze_transits(transit_pos, asc_sign, target_houses, category="Career"):
    observations = []
    for planet in ["Jupiter", "Saturn", "Rahu", "Ketu"]:
        t_pos = transit_pos.get(planet)
        if not t_pos: continue
        t_sign = get_planet_sign(t_pos)
        t_house = calculate_house(t_sign, asc_sign)
        if not t_house: continue
        if t_house in target_houses:
            outcome = get_house_outcome(t_house, type='pos' if planet == 'Jupiter' else 'neg', category=category)
            observations.append(f"<b>Current Transit:</b> Moving {planet} is currently activating <b>{outcome}</b>.")
    return observations

def analyze_jamakkol(jamakkol_data, asc_sign, category_houses, category="Career"):
    observations = []
    if not jamakkol_data: return []
    udayam = jamakkol_data.get('Udayam')
    arudham = jamakkol_data.get('Arudham')
    kavippu = jamakkol_data.get('Kavippu')
    if udayam:
        u_house = calculate_house(udayam, asc_sign)
        if u_house in category_houses:
             observations.append(f"<b>Immediate Focus:</b> Current energy is high for <b>{get_house_outcome(u_house, category=category)}</b>. Action taken now will bring results.")
    if arudham:
        a_house = calculate_house(arudham, asc_sign)
        if a_house in category_houses:
             observations.append(f"<b>Outcome Hint:</b> Indicators suggest a favorable path regarding <b>{get_house_outcome(a_house, type='pos', category=category)}</b>.")
    if kavippu:
        k_house = calculate_house(kavippu, asc_sign)
        if k_house in category_houses:
             observations.append(f"<b>Caution:</b> Temporary hurdles are present in <b>{get_house_outcome(k_house, type='neg', category=category)}</b>. Patience is advised.")
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
        observations.append(f"<b>Bhukti (Current Sub-Cycle):</b> The {b_lord} sub-period is active, bringing a focus on <b>{focus}</b> to your {category_name.lower()} matters.")
        
    return observations
