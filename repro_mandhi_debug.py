import sys
import os
import swisseph as swe
from datetime import datetime, timedelta

# Add current directory to path
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'astro_predictor_app'))

from astro_predictor_app.app.schemas import BirthDetails
# We will copy the logic to play with it
from astro_predictor_app.app.services.astrology_engine import astrology_engine

def debug_mandhi():
    lat = 12.6936
    lon = 79.9769
    date_str = "2009-04-09"
    time_str = "22:58:00"
    timezone = 5.5
    
    dt_local = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
    dt_utc = dt_local - timedelta(hours=timezone)
    jd_utc = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute/60.0 + dt_utc.second/3600.0)
    
    # 1. Calculate Standard Mandhi (Current Code)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    ayanamsa = swe.get_ayanamsa_ut(jd_utc)
    sign_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                  "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
                  
    print(f"--- Debugging Mandhi Calculation ---")
    print(f"Input: {dt_local}, Lat: {lat}, Lon: {lon}")
    
    # Extract Logic
    year, month, day, hour = swe.revjul(jd_utc)
    jd_start = swe.julday(year, month, day, 0)
    
    def get_sun_alt(jd, target_refraction=True):
        res_equ = swe.calc_ut(jd, swe.SUN, swe.FLG_EQUATORIAL)
        ra = float(res_equ[0][0])
        dec = float(res_equ[0][1])
        res_hor = swe.azalt(jd, swe.EQU2HOR, [float(lon), float(lat), 0.0], 0.0, 0.0, [ra, dec, 1.0])
        return float(res_hor[1])

    def find_crossing(jd_start, jd_end, target_alt=-0.8333):
        low, high = jd_start, jd_end
        for _ in range(20):
            mid = (low + high) / 2
            alt_mid = get_sun_alt(mid)
            if (alt_mid > target_alt) == (get_sun_alt(low) > target_alt):
                low = mid
            else:
                high = mid
        return (low + high) / 2

    jd_rise = find_crossing(jd_start, jd_start + 0.5)
    jd_set = find_crossing(jd_start + 0.5, jd_start + 1.0)
    
    print(f"Sunrise JD: {jd_rise}")
    print(f"Sunset JD: {jd_set}")
    
    # Determine Day/Night
    y, m, d, h = swe.revjul(jd_utc)
    dt_date = datetime(y, m, d)
    dow = (dt_date.weekday() + 1) % 7
    is_day = jd_rise <= jd_utc <= jd_set
    
    print(f"Day of Week: {dow} (0=Sun, 4=Thu)")
    print(f"Is Day Birth: {is_day}")
    
    day_offsets = [26, 22, 18, 14, 10, 6, 2]
    night_offsets = [10, 6, 2, 26, 22, 18, 14]
    ghatika = day_offsets[dow] if is_day else night_offsets[dow]
    
    print(f"Ghatika: {ghatika}")
    
    if is_day:
        duration_jd = jd_set - jd_rise
        start_jd = jd_rise
    else:
        jd_next_rise = find_crossing(jd_set, jd_set + 0.5)
        duration_jd = jd_next_rise - jd_set
        start_jd = jd_set

    # MANDHI TIME
    mandhi_jd = start_jd + (ghatika / 30.0) * duration_jd
    
    # Calculate Position
    houses, ascmc = swe.houses_ex(mandhi_jd, lat, lon, b'P')
    m_trop = ascmc[0]
    m_sid = (m_trop - ayanamsa) % 360
    
    print(f"Calculated Mandhi Longitude: {m_sid}")
    print(f"In Sign: {sign_names[int(m_sid//30)]} {m_sid%30}")
    
    # Target Information
    target_lon = 300.38 # Aquarius 0.23
    diff = target_lon - m_sid
    print(f"Target: {target_lon}")
    print(f"Diff: {diff} degrees")
    
    # Sensitivity Analysis
    # How much time shift corresponds to this diff?
    # Ascendant moves 360 deg in 1 day (roughly). 
    # Velocity at that time?
    h_next, a_next = swe.houses_ex(mandhi_jd + 0.001, lat, lon, b'P') # +1.4 mins
    vel = (a_next[0] - m_trop) / 0.001 # deg per day
    print(f"Ascendant Velocity: {vel} deg/day")
    
    needed_time_shift_days = diff / vel
    needed_time_shift_mins = needed_time_shift_days * 1440
    print(f"Needed Time Shift: {needed_time_shift_mins} mins")
    
    # Testing Alternative Sunrise/Sunset using swe.rise_trans
    
    # Check flags
    # standard = upper limb + refraction
    rsmi_rise = swe.CALC_RISE
    rsmi_set = swe.CALC_SET
    
    # Try Standard
    geopos = (float(lon), float(lat), 0.0)
    
    # Find sunrise on day
    # Start search from midnight - 12h to ensure we catch it?
    # actually jd_start is midnight. Sunrise is after.
    
    def test_swe_rise_trans(flag_extra=0, name="swe.rise_trans"):
        try:
            res_rise = swe.rise_trans(jd_start, swe.SUN, rsmi_rise | flag_extra, geopos, 0, 0, swe.FLG_SWIEPH)
            trise = res_rise[1][0]
            
            res_set = swe.rise_trans(trise + 0.01, swe.SUN, rsmi_set | flag_extra, geopos, 0, 0, swe.FLG_SWIEPH)
            tset = res_set[1][0]
            
            # Next rise
            res_next_rise = swe.rise_trans(tset + 0.01, swe.SUN, rsmi_rise | flag_extra, geopos, 0, 0, swe.FLG_SWIEPH)
            tnext_rise = res_next_rise[1][0]
            
            if is_day:
                dur = tset - trise
                st = trise
            else:
                dur = tnext_rise - tset
                st = tset
                
            mjd = st + (ghatika/30.0)*dur
            h, a = swe.houses_ex(mjd, lat, lon, b'P')
            m_trop = a[0]
            ms = (m_trop - ayanamsa) % 360
            
            print(f"--- Option: {name} ---")
            print(f"Mandhi JD: {mjd}")
            print(f"Result Lon: {ms}")
            print(f"Diff from Target: {target_lon - ms}")
        except Exception as e:
            print(f"Error in {name}: {e}")

    test_swe_rise_trans(0, "Standard swe.rise_trans (Upper Limb)")
    test_swe_rise_trans(swe.BIT_DISC_CENTER, "Center of Disc")
    test_swe_rise_trans(swe.BIT_NO_REFRACTION, "No Refraction")
    test_swe_rise_trans(swe.BIT_DISC_CENTER | swe.BIT_NO_REFRACTION, "Center Geometric")


if __name__ == "__main__":
    debug_mandhi()

