import sys
import os
import swisseph as swe

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from astro_predictor_app.app.services.astrology_engine import astrology_engine
    from astro_predictor_app.app.schemas import BirthDetails
except ImportError:
    sys.path.append(os.path.join(os.getcwd(), 'astro_predictor_app'))
    from astro_predictor_app.app.services.astrology_engine import astrology_engine
    from astro_predictor_app.app.schemas import BirthDetails

def to_dms(deg_float):
    d = int(deg_float)
    m = int((deg_float - d) * 60)
    s = int(((deg_float - d) * 60 - m) * 60)
    return f"{d}° {m}' {s}\""

def analyze_raja():
    details = BirthDetails(
        name="RAJAGOPAL KANNAN",
        date_of_birth="1972-03-23",
        time_of_birth="09:00:00",
        place_of_birth="Bengaluru, Karnataka, India",
        latitude=12.9716,
        longitude=77.5946,
        timezone=5.5
    )
    
    print(f"Calculating chart for {details.date_of_birth} {details.time_of_birth}")
    chart = astrology_engine.calculate_chart(details)
    
    print(f"Rasi Ascendant: {chart.get('ascendant')}")
    print("Planets:", chart.get('planetary_positions'))
    print(f"Navamsa Ascendant (Current): {chart.get('navamsa_ascendant')}")
    
    lat = 12.9716
    lon = 77.5946
    sign_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                  "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

    # Analyze when Ascendant is Sagittarius
    print("\n--- Searching for Sagittarius Ascendant ---")
    start_jd = swe.julday(1972, 3, 23, 0) # Midnight
    jd_base = swe.julday(1972, 3, 23, 3.5 + 0/60.0) # 09:00 Local
    for h in range(0, 24):
        jd = start_jd + h/24.0
        houses, ascmc = swe.houses_ex(jd, lat, lon, b'P')
        asc = ascmc[0]
        base_ayan = swe.get_ayanamsa_ut(jd)
        asc_sid = (asc - base_ayan) % 360
        asc_sign = sign_names[int(asc_sid // 30)]
        
        if asc_sign == "Sagittarius":
            print(f"Sagittarius Ascendant found around {h}:00 hours")

    # Check Timezone = 0 (09:00 UTC input)
    # If user sent 09:00 and timezone 0.
    # Then dt_utc = 09:00.
    # jd_utc for 09:00 UT.
    jd_utc_0 = swe.julday(1972, 3, 23, 9.0 + 0/60.0)
    
    houses, ascmc = swe.houses_ex(jd_utc_0, lat, lon, b'P')
    asc = ascmc[0]
    base_ayan = swe.get_ayanamsa_ut(jd_utc_0)
    asc_sid = (asc - base_ayan) % 360
    nav_lon = (asc_sid * 9) % 360
    nav_sign = sign_names[int(nav_lon // 30)]
    print(f"\nAt 09:00 UTC (Timezone=0): Nav Ascendant is {nav_sign} ({to_dms(nav_lon%30)})")
    
    # Check Timezone = -5 (09:00 Local -> 14:00 UTC)
    # Hypothesis: East longitude treated as West.
    jd_utc_neg5 = swe.julday(1972, 3, 23, 14.0 + 0/60.0)
    
    houses, ascmc = swe.houses_ex(jd_utc_neg5, lat, lon, b'P')
    asc = ascmc[0]
    base_ayan = swe.get_ayanamsa_ut(jd_utc_neg5)
    asc_sid = (asc - base_ayan) % 360
    nav_lon = (asc_sid * 9) % 360
    nav_sign = sign_names[int(nav_lon // 30)]
    print(f"\nAt 14:00 UTC (Timezone=-5): Nav Ascendant is {nav_sign} ({to_dms(nav_lon%30)})")
    
    # Check Latitude Swipe (12.97 S)
    houses, ascmc = swe.houses_ex(jd_base, -12.9716, lon, b'P')
    asc = ascmc[0]
    base_ayan = swe.get_ayanamsa_ut(jd_base)
    asc_sid = (asc - base_ayan) % 360
    nav_lon = (asc_sid * 9) % 360
    nav_sign = sign_names[int(nav_lon // 30)]
    print(f"At 12.97 S (Latitude Flip): Nav Ascendant is {nav_sign} ({to_dms(nav_lon%30)})")
    
    # Check Suryasiddhanta Ayanamsa
    swe.set_sid_mode(swe.SIDM_SURYASIDDHANTA)
    houses, ascmc = swe.houses_ex(jd_base, lat, lon, b'P')
    asc = ascmc[0]
    base_ayan = swe.get_ayanamsa_ut(jd_base)
    asc_sid = (asc - base_ayan) % 360
    nav_lon = (asc_sid * 9) % 360
    nav_sign = sign_names[int(nav_lon // 30)]
    print(f"Suryasiddhanta: Nav Ascendant is {nav_sign} ({to_dms(nav_lon%30)})")
    
    # Check Tropical (Sayana)
    # Don't subtract Ayanamsa
    houses, ascmc = swe.houses_ex(jd_base, lat, lon, b'P')
    asc_trop = ascmc[0]
    nav_lon_trop = (asc_trop * 9) % 360
    nav_sign_trop = sign_names[int(nav_lon_trop // 30)]
    print(f"Tropical (Sayana): Nav Ascendant is {nav_sign_trop} ({to_dms(nav_lon_trop%30)})")

    # Check Stale Coordinates (Chengalpattu from Sample Report)
    lat_sample = 12.6936
    lon_sample = 79.9769
    houses, ascmc = swe.houses_ex(jd_base, lat_sample, lon_sample, b'P')
    asc = ascmc[0]
    base_ayan = swe.get_ayanamsa_ut(jd_base)
    asc_sid = (asc - base_ayan) % 360
    nav_lon = (asc_sid * 9) % 360
    nav_sign = sign_names[int(nav_lon // 30)]
    print(f"Using Chengalpattu (Sample) Coords: Nav Ascendant is {nav_sign} ({to_dms(nav_lon%30)})")

    # Check "Approximated" Timezone (Frontend Logic)
    # Bengaluru Longitude 77.59. 
    # Frontend: round((77.59 * 4 / 60) * 10) / 10 = round(5.17) = 5.2
    tz_approx = 5.2
    # 09:00 Local - 5.2 = 03:48 UTC.
    # Standard was 09:00 - 5.5 = 03:30 UTC.
    # So we are feeding a time that is 18 minutes LATER in absolute terms? 
    # No, we feed Local Time + Timezone. 
    # Engine does: UTC = Local - Timezone.
    # UTC_used = 09:00 - 5.2 = 03:48.
    # Real UTC = 03:30.
    # So we are running the calculation for 03:48 UTC (Real UTC + 18 mins).
    # This means the planets/ascendant are calculated for 18 minutes LATER.
    
    jd_tz_err = swe.julday(1972, 3, 23, 9.0 - tz_approx + 0/60.0)
    houses, ascmc = swe.houses_ex(jd_tz_err, lat, lon, b'P')
    asc = ascmc[0]
    base_ayan = swe.get_ayanamsa_ut(jd_tz_err)
    asc_sid = (asc - base_ayan) % 360
    nav_lon = (asc_sid * 9) % 360
    nav_sign = sign_names[int(nav_lon // 30)]
    print(f"\n--- Timezone Approx Error Check (TZ=5.2) ---")
    print(f"Using TZ 5.2: Nav Ascendant is {nav_sign} ({to_dms(nav_lon%30)})")

if __name__ == "__main__":
    analyze_raja()
