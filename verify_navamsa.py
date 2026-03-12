import swisseph as swe
from datetime import datetime, timedelta

def to_dms(deg_float):
    d = int(deg_float)
    m = int((deg_float - d) * 60)
    s = int(((deg_float - d) * 60 - m) * 60)
    return f"{d}° {m}' {s}\""

def get_sign_name(lon):
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    return signs[int(lon // 30)]

def calc_ascendant(ayanamsa_mode, mode_name):
    # Location
    lat = 12.6936
    lon = 79.9769
    
    # Time
    dt_str = "2009-04-09 22:58:00"
    dt_local = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    dt_utc = dt_local - timedelta(hours=5.5)
    
    jd_utc = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute/60.0 + dt_utc.second/3600.0)
    
    # Set Ayanamsa
    swe.set_sid_mode(ayanamsa_mode)
    base_ayan = swe.get_ayanamsa_ut(jd_utc)
    
    
    # Calculate Houses
    # 1. Geocentric
    houses, ascmc = swe.houses_ex(jd_utc, lat, lon, b'P')
    asc_geoc = ascmc[0]
    asc_geoc_sid = (asc_geoc - base_ayan) % 360
    nav_geoc = (asc_geoc_sid * 9) % 360
    
    # 2. Topocentric
    swe.set_topo(lon, lat, 0)
    houses, ascmc = swe.houses_ex(jd_utc, lat, lon, b'P')
    asc_topo = ascmc[0]
    asc_topo_sid = (asc_topo - base_ayan) % 360
    nav_topo = (asc_topo_sid * 9) % 360
    
    print(f"--- {mode_name} ---")
    print(f"Geo Navamsa: {get_sign_name(nav_geoc)} {to_dms(nav_geoc % 30)}")
    print(f"Topo Navamsa: {get_sign_name(nav_topo)} {to_dms(nav_topo % 30)}")

    # Sensitivity (Time + 1 min)
    jd_plus = jd_utc + (1.0/1440.0)
    houses, ascmc = swe.houses_ex(jd_plus, lat, lon, b'P') # Geo
    asc_p = (ascmc[0] - base_ayan) % 360
    nav_p = (asc_p * 9) % 360
    print(f"Time +1m Navamsa: {get_sign_name(nav_p)} {to_dms(nav_p % 30)}")
    
    # Sensitivity (Time + 54s approx 0.9 min)
    # 54s = 54/86400 days ? No. 1 min = 1/1440 days. 1 sec = 1/86400.
    # 54s = 54/86400.
    jd_54s = jd_utc + (54.0/86400.0)
    houses, ascmc = swe.houses_ex(jd_54s, lat, lon, b'P') # Geo
    asc_54 = (ascmc[0] - base_ayan) % 360
    nav_54 = (asc_54 * 9) % 360
    print(f"Time +54s Navamsa: {get_sign_name(nav_54)} {to_dms(nav_54 % 30)}")

print("Calculating Ascendant Sensitivity...")
calc_ascendant(swe.SIDM_LAHIRI, "Lahiri")
calc_ascendant(swe.SIDM_KRISHNAMURTI, "KP")
