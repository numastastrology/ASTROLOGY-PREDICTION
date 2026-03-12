from astro_predictor_app.app.schemas import BirthDetails
from typing import Dict, Any, List, Optional
import swisseph as swe
from datetime import datetime, timedelta
import math

class AstrologyEngine:
    def __init__(self):
        # Swiss Ephemeris initialization
        # Default is Moshier, but we use built-in planetary files if they exist.
        pass

    def calculate_chart(self, birth_details: BirthDetails) -> Dict[str, Any]:
        """
        Calculates natal chart using Swiss Ephemeris (Sidereal Lahiri).
        """
        # 1. Parse Time and Location
        try:
            print(f"DEBUG: Received BirthDetails for {birth_details.name}")
            dt_str = f"{birth_details.date_of_birth} {birth_details.time_of_birth}"
            dt_local = None
            for fmt in ["%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%d-%m-%Y %H:%M", "%d/%m/%Y %H:%M"]:
                try:
                    dt_local = datetime.strptime(dt_str, fmt)
                    break
                except: continue
            
            if not dt_local: raise ValueError("Could not parse Date/Time")
            
            offset = float(birth_details.timezone if birth_details.timezone is not None else 5.5)
            dt_utc = dt_local - timedelta(hours=offset)
            
            # Julian Day for Swiss Ephemeris
            jd_utc = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute/60.0 + dt_utc.second/3600.0)
        except Exception as e:
            print(f"Error parsing date in calculate_chart: {e}")
            return {"error": str(e)}

        lat = float(birth_details.latitude)
        lon = float(birth_details.longitude)

        # 2. Configure Sidereal Mode (Lahiri)
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        ayanamsa = swe.get_ayanamsa_ut(jd_utc)
        
        print(f"DEBUG: Lat={lat}, Lon={lon}, TZ={offset}")
        print(f"DEBUG: JD_UTC={jd_utc}, DateUTC={dt_utc}")
        print(f"DEBUG: Ayanamsa={ayanamsa}")

        sign_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                      "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

        planet_map = {
            swe.SUN: "Sun",
            swe.MOON: "Moon",
            swe.MERCURY: "Mercury",
            swe.VENUS: "Venus",
            swe.MARS: "Mars",
            swe.JUPITER: "Jupiter",
            swe.SATURN: "Saturn",
            swe.MEAN_NODE: "Rahu"
        }

        DEBILITATION_MAP = {
            'Sun': 'Libra', 'Moon': 'Scorpio', 'Mars': 'Cancer', 'Mercury': 'Pisces',
            'Jupiter': 'Capricorn', 'Venus': 'Virgo', 'Saturn': 'Aries',
            'Rahu': 'Scorpio', 'Ketu': 'Taurus'
        }

        COMBUSTION_ORBS = {
            'Moon': 12, 'Mars': 17, 'Mercury': 14, 'Jupiter': 11, 'Venus': 10, 'Saturn': 15
        }

        planetary_positions = {}
        navamsa_positions = {}
        
        # Flags: Sidereal + Speed (for retrograde)
        flags = swe.FLG_SIDEREAL | swe.FLG_SPEED

        # Get Sun position for combustion check
        sun_res, _ = swe.calc_ut(jd_utc, swe.SUN, flags)
        sun_lon_sid = sun_res[0]

        for p_id, name in planet_map.items():
            res, _ = swe.calc_ut(jd_utc, p_id, flags)
            lon_sid = res[0]
            speed = res[3]
            
            # Status Check
            is_retro = speed < 0 if name not in ["Rahu", "Ketu"] else True
            
            is_combust = False
            if name != "Sun" and name in COMBUSTION_ORBS:
                dist = abs((lon_sid - sun_lon_sid + 180) % 360 - 180)
                if dist < COMBUSTION_ORBS[name]: is_combust = True
            
            sign_idx = int(lon_sid // 30)
            is_debil = DEBILITATION_MAP.get(name) == sign_names[sign_idx]
            
            status = ""
            if is_retro and name not in ["Sun", "Moon"]: status += " (R)"
            if is_combust: status += " (C)"
            if is_debil: status += " (D)"
            
            deg = int(lon_sid % 30)
            minute = int((lon_sid % 1) * 60)
            planetary_positions[name] = f"{sign_names[sign_idx]} ({deg}° {minute}'){status}"
            
            # Navamsa (D9)
            d9_lon = (lon_sid * 9) % 360
            d9_sign_idx = int(d9_lon // 30)
            is_d9_debil = DEBILITATION_MAP.get(name) == sign_names[d9_sign_idx]
            
            d9_status = ""
            if is_retro and name not in ["Sun", "Moon"]: d9_status += " (R)"
            if is_combust: d9_status += " (C)"
            if is_d9_debil: d9_status += " (D)"
            
            d9_deg = int(d9_lon % 30)
            d9_min = int((d9_lon % 1) * 60)
            navamsa_positions[name] = f"{sign_names[d9_sign_idx]} ({d9_deg}° {d9_min}'){d9_status}"

        # Ketu calculation
        rahu_res, _ = swe.calc_ut(jd_utc, swe.MEAN_NODE, flags)
        rahu_lon = rahu_res[0]
        ketu_lon = (rahu_lon + 180) % 360
        k_sign_idx = int(ketu_lon // 30)
        k_debil = DEBILITATION_MAP.get('Ketu') == sign_names[k_sign_idx]
        k_status = " (R)" + (" (D)" if k_debil else "")
        planetary_positions["Ketu"] = f"{sign_names[k_sign_idx]} ({int(ketu_lon % 30)}° {int((ketu_lon % 1)*60)}'){k_status}"
        
        kd9_lon = (ketu_lon * 9) % 360
        kd9_idx = int(kd9_lon // 30)
        kd9_debil = DEBILITATION_MAP.get('Ketu') == sign_names[kd9_idx]
        kd9_status = " (R)" + (" (D)" if kd9_debil else "")
        navamsa_positions["Ketu"] = f"{sign_names[kd9_idx]} ({int(kd9_lon % 30)}° {int((kd9_lon % 1)*60)}'){kd9_status}"

        # 3. Houses / Ascendant
        houses, ascmc = swe.houses_ex(jd_utc, lat, lon, b'P') 
        asc_trop = ascmc[0]
        asc_sid = (asc_trop - ayanamsa) % 360
        asc_idx = int(asc_sid // 30)
        ascendant = sign_names[asc_idx]
        
        # Precise D9 Ascendant
        asc_d9_lon = (asc_sid * 9) % 360
        d9_asc_idx = int(asc_d9_lon // 30)
        d9_asc_deg = int(asc_d9_lon % 30)
        d9_asc_min = int((asc_d9_lon % 1) * 60)
        d9_ascendant = f"{sign_names[d9_asc_idx]} ({d9_asc_deg}° {d9_asc_min}')"
        
        # 4. Nakshatra
        NAKSHATRA_NAMES = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
            "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
            "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]
        month_lon_res, _ = swe.calc_ut(jd_utc, swe.MOON, flags)
        moon_lon_sid = month_lon_res[0]
        nak_idx = int(moon_lon_sid / (360/27.0))
        star_name = NAKSHATRA_NAMES[nak_idx % 27]
        pada_num = int((moon_lon_sid % (360/27.0)) / (360/27.0/4.0)) + 1
        
        # 5. Mandhi / Transit / Jamakkol
        # Mandhi
        try:
             # Calculate Mandhi position (middle of Saturn's Yamam)
             # Use Geometric Sunrise (Center of Disc, No Refraction) to match user expectations
             m_sign, m_deg, m_min = self._calculate_mandhi_swe(jd_utc, lat, lon, ayanamsa, sign_names)
             planetary_positions['Mandhi'] = f"{m_sign} ({m_deg}° {m_min}')"
             if m_sign in sign_names:
                 m_idx = sign_names.index(m_sign)
                 m_lon = (m_idx * 30) + m_deg + (m_min/60.0)
                 m_d9 = (m_lon * 9) % 360
                 navamsa_positions['Mandhi'] = f"{sign_names[int(m_d9//30)]} ({int(m_d9%30)}° {int((m_d9%1)*60)}')"
             else:
                  navamsa_positions['Mandhi'] = "Unknown"
        except Exception as e:
              print(f"Mandhi error: {e}")
              planetary_positions['Mandhi'] = "Error"
              navamsa_positions['Mandhi'] = "Error"

        # Transit (at current time)
        transit_positions = {}
        try:
            jd_now = swe.julday(datetime.now().year, datetime.now().month, datetime.now().day, 
                                datetime.now().hour + datetime.now().minute/60.0)
            ayan_now = swe.get_ayanamsa_ut(jd_now)
            for p_id, name in planet_map.items():
                 t_res, _ = swe.calc_ut(jd_now, p_id, flags)
                 t_lon = (t_res[0])
                 t_idx = int(t_lon // 30)
                 transit_positions[name] = f"{sign_names[t_idx]} ({int(t_lon%30)}° {int((t_lon%1)*60)}')"
            
            # Ketu Transit
            tr_res, _ = swe.calc_ut(jd_now, swe.MEAN_NODE, flags)
            tr_lon = tr_res[0]
            tk_lon = (tr_lon + 180) % 360
            transit_positions["Ketu"] = f"{sign_names[int(tk_lon//30)]} ({int(tk_lon%30)}° {int((tk_lon%1)*60)}')"
        except: pass

        return {
            "name": birth_details.name,
            "date_of_birth": birth_details.date_of_birth,
            "time_of_birth": birth_details.time_of_birth,
            "place_of_birth": birth_details.place_of_birth,
            "ascendant": ascendant,
            "navamsa_ascendant": d9_ascendant,
            "planetary_positions": planetary_positions,
            "navamsa_positions": navamsa_positions,
            "transit_positions": transit_positions,
            "ayanamsa": f"{int(ayanamsa)}° {int((ayanamsa%1)*60)}'",
            "nakshatra": star_name,
            "pada": str(pada_num),
            "jamakkol": self._calculate_jamakkol_basic(lat, lon, ayanamsa, sign_names)
        }

    def _calculate_jamakkol_basic(self, lat, lon, ayanamsa, sign_names):
        """
        Basic Jamakkol Prasannam calculation based on current time.
        Udayam: Ascendant at current time.
        Arudham: Moon sign at current time (Approximation for now).
        Kavippu: Udayam + 180 degrees (Opposition).
        """
        try:
             now = datetime.now()
             jd_now = swe.julday(now.year, now.month, now.day, now.hour + now.minute/60.0)
             
             # Udayam (Ascendant)
             houses, ascmc = swe.houses_ex(jd_now, lat, lon, b'P')
             asc_trop = ascmc[0]
             asc_sid = (asc_trop - ayanamsa) % 360
             
             # Arudham (Moon for now)
             # In real Jamakkol, Arudham is based on Arooda Number or Clock.
             # We use Moon as a temporary substitute if logic is missing.
             res, _ = swe.calc_ut(jd_now, swe.MOON, swe.FLG_SIDEREAL | swe.FLG_SPEED)
             moon_lon = res[0]
             
             # Kavippu (Opposition to Udayam - simplifed rule)
             kavippu_lon = (asc_sid + 180) % 360
             
             def to_str(lon):
                 idx = int(lon // 30)
                 return sign_names[idx]
             
             return {
                 "Udayam": to_str(asc_sid),
                 "Arudham": to_str(moon_lon),
                 "Kavippu": to_str(kavippu_lon)
             }
        except Exception as e:
             print(f"Jamakkol error: {e}")
             return {}

    def _calculate_mandhi_swe(self, jd_utc, lat, lon, ayanamsa, sign_names):
        # 1. Precise Sunrise/Sunset calculation for Mandhi (Geometric: Center, No Refraction)
        try:
            # 1. Get Sunrise/Sunset using swisseph
            # Note: swe.rise_trans requires (tjd, planet, flag, geopos, atpress, attemp, calc_flag)
            # geopos = (lon, lat, height)
            geopos = (float(lon), float(lat), 0.0)
            
            # Flags for Geometric Sunrise (Center of Disc, No Refraction)
            rsmi_rise = swe.CALC_RISE | swe.BIT_DISC_CENTER | swe.BIT_NO_REFRACTION
            rsmi_set = swe.CALC_SET | swe.BIT_DISC_CENTER | swe.BIT_NO_REFRACTION
            
            # Start searching from (jd_utc - 1) to ensure we find the cycle containing birth
            base_jd = jd_utc - 1.0
            
            res_rise = swe.rise_trans(base_jd, swe.SUN, rsmi_rise, geopos, 0, 0, swe.FLG_SWIEPH)
            rise_1 = res_rise[1][0]
            
            res_set = swe.rise_trans(rise_1 + 0.01, swe.SUN, rsmi_set, geopos, 0, 0, swe.FLG_SWIEPH)
            set_1 = res_set[1][0]
            
            res_rise2 = swe.rise_trans(set_1 + 0.01, swe.SUN, rsmi_rise, geopos, 0, 0, swe.FLG_SWIEPH)
            rise_2 = res_rise2[1][0]
            
            res_set2 = swe.rise_trans(rise_2 + 0.01, swe.SUN, rsmi_set, geopos, 0, 0, swe.FLG_SWIEPH)
            set_2 = res_set2[1][0]
            
            # Identify the correct day/night segment
            if rise_1 <= jd_utc <= set_1:
                 # Day birth (Cycle 1)
                 start_jd = rise_1
                 end_jd = set_1
                 is_day = True
                 final_rise_for_wd = rise_1
            elif set_1 <= jd_utc <= rise_2:
                 # Night birth (Cycle 1)
                 start_jd = set_1
                 end_jd = rise_2
                 is_day = False
                 final_rise_for_wd = rise_1 # Night belongs to day starting at rise_1
            elif rise_2 <= jd_utc <= set_2:
                 # Day birth (Cycle 2)
                 start_jd = rise_2
                 end_jd = set_2
                 is_day = True
                 final_rise_for_wd = rise_2
            else:
                 # Fallback (e.g. just before rise_1)
                 # Should theoretically be previous night.
                 # Let's assume Cycle 1 for safety or expand search if needed.
                 # Given lookback of 1 day, rise_1 is usually ~18h before jd_utc or ~6h before
                 start_jd = rise_1
                 end_jd = set_1
                 is_day = True
            # Weekday calculation
            # swe.day_of_week returns 0=Mon, 1=Tue... 6=Sun
            wd = swe.day_of_week(final_rise_for_wd)
            
            # day_offsets is [Sun, Mon, Tue, Wed, Thu, Fri, Sat]
            # We need to map swe(0=Mon) -> Index 1
            # swe(6=Sun) -> Index 0
            wd_idx = (wd + 1) % 7
            
            day_offsets = [26, 22, 18, 14, 10, 6, 2] # Sun..Sat
            night_offsets = [10, 6, 2, 26, 22, 18, 14]
            
            ghatika = day_offsets[wd_idx] if is_day else night_offsets[wd_idx]
            
            duration_jd = end_jd - start_jd
            # Mandhi time formula: start + (ghatika / 30) * duration_jd
            mandhi_jd = start_jd + (ghatika / 30.0) * duration_jd
            
            # Mandhi time formula: start + (ghatika / 30) * duration_jd
            mandhi_jd = start_jd + (ghatika / 30.0) * duration_jd
            
            # Mandhi longitude
            houses, ascmc = swe.houses_ex(mandhi_jd, lat, lon, b'P')
            m_trop = ascmc[0]
            m_sid = (m_trop - ayanamsa) % 360
            
            sign_idx = int(m_sid // 30)
            deg = int(m_sid % 30)
            minute = int((m_sid % 1) * 60)
            return sign_names[sign_idx], deg, minute
        except Exception as e:
            print(f"Inner Mandhi calculation error: {e}")
            return "Unknown", 0, 0

    def calculate_vimshottari_dasa(self, birth_details: BirthDetails, chart_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Parsing Moon position from planetary_positions
        sign_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                      "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        moon_str = chart_data['planetary_positions']['Moon']
        m_sign_str = moon_str.split('(')[0].strip()
        m_deg_str = moon_str.split('(')[1].split(')')[0]
        m_deg = int(m_deg_str.split('°')[0])
        m_min = int(m_deg_str.split('°')[1].replace("'", "").strip())
        moon_lon = (sign_names.index(m_sign_str) * 30) + m_deg + (m_min/60.0)

        nakshatras_lords = [("Ketu", 7), ("Venus", 20), ("Sun", 6), ("Moon", 10), ("Mars", 7), ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19), ("Mercury", 17)] * 3
        moon_minutes = moon_lon * 60
        nak_idx = int(moon_minutes / 800)
        elapsed = moon_minutes % 800
        balance_frac = (800 - elapsed) / 800.0
        
        dt_str = f"{birth_details.date_of_birth} {birth_details.time_of_birth}"
        dob = None
        for fmt in ["%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%d-%m-%Y %H:%M", "%d/%m/%Y %H:%M"]:
            try:
                dob = datetime.strptime(dt_str, fmt)
                break
            except: continue
        
        if not dob:
            dob = datetime.now() # Fallback
        
        dasas = []
        curr = dob
        for i in range(9):
             lord, years = nakshatras_lords[(nak_idx + i) % 27]
             if i == 0: duration = years * balance_frac
             else: duration = years
             
             end = curr + timedelta(days=duration * 365.25)
             dasas.append({"lord": lord, "start": curr.strftime("%d-%m-%Y"), "end": end.strftime("%d-%m-%Y")})
             curr = end
        return dasas

    def get_current_dasa_bhukti(self, dasas, target_date_str=None):
        target = datetime.strptime(target_date_str, "%Y-%m-%d") if target_date_str else datetime.now()
        cur_d = next((d for d in dasas if datetime.strptime(d['start'], "%d-%m-%Y") <= target <= datetime.strptime(d['end'], "%d-%m-%Y")), None)
        if not cur_d: return {}
        
        order = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
        years = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}
        
        d_lord = cur_d['lord']
        d_years = years[d_lord]
        d_start = datetime.strptime(cur_d['start'], "%d-%m-%Y")
        d_end = datetime.strptime(cur_d['end'], "%d-%m-%Y")
        
        # Total days in this Dasa (using actual calendar range)
        dasa_total_days = (d_end - d_start).total_seconds() / 86400.0
        
        # 1. Bhukti calculation
        start_idx = order.index(d_lord)
        b_curr = d_start
        for i in range(9):
             b_lord = order[(start_idx + i) % 9]
             # Bhukti fraction of the Dasa
             b_frac = years[b_lord] / 120.0
             b_duration_days = dasa_total_days * b_frac
             b_end = b_curr + timedelta(days=b_duration_days)
             
             # Adjust last Bhukti to exactly match Dasa end
             if i == 8: b_end = d_end
             
             if b_curr <= target <= b_end:
                  # 2. Antara calculation
                  a_start_idx = order.index(b_lord)
                  a_curr = b_curr
                  bhukti_total_days = (b_end - b_curr).total_seconds() / 86400.0
                  
                  for j in range(9):
                      a_lord = order[(a_start_idx + j) % 9]
                      # Antara fraction of the Bhukti
                      a_frac = years[a_lord] / 120.0
                      a_duration_days = bhukti_total_days * a_frac
                      a_end = a_curr + timedelta(days=a_duration_days)
                      
                      # Adjust last Antara to exactly match Bhukti end
                      if j == 8: a_end = b_end
                      
                      if a_curr <= target <= a_end:
                           return {
                               "dasa": cur_d,
                               "bhukti": {
                                   "lord": b_lord, 
                                   "start": b_curr.strftime("%d-%m-%Y"), 
                                   "end": b_end.strftime("%d-%m-%Y")
                               },
                               "antara": {
                                   "lord": a_lord, 
                                   "start": a_curr.strftime("%d-%m-%Y"), 
                                   "end": a_end.strftime("%d-%m-%Y")
                               }
                           }
                      a_curr = a_end
                  
                  return {
                      "dasa": cur_d, 
                      "bhukti": {"lord": b_lord, "start": b_curr.strftime("%d-%m-%Y"), "end": b_end.strftime("%d-%m-%Y")}
                  }
             b_curr = b_end
        return {"dasa": cur_d}

    def generate_all_predictions(self, birth_details, chart_data, selected_categories=None):
        if "error" in chart_data:
             return {cat: {"points": [f"Error in chart calculation: {chart_data['error']}"], "score": 0} 
                     for cat in (selected_categories or ["health"])}

        from astro_predictor_app.app.services.category_logic import (
            health, career, finance, stock_market, foreign_settlement,
            relationships, children, education, spirituality, legal,
            house_property, land_real_estate, vehicles, business_vs_job,
            promotion, luck_factor, job_change, business_start_change, dasa_predictions, native as native_characteristics
        )
        cat_map = {
            "health": health, "career": career, "finance": finance, "stock_market": stock_market,
            "foreign_settlement": foreign_settlement, "relationships": relationships, "children": children,
            "education": education, "spirituality": spirituality, "legal": legal,
            "house_property": house_property, "land_real_estate": land_real_estate, "vehicles": vehicles,
            "business_vs_job": business_vs_job, "promotion": promotion, "luck_factor": luck_factor,
            "job_change": job_change, "business_start_change": business_start_change, "dasa_predictions": dasa_predictions,
            "native_characteristics": native_characteristics
        }
        
        try:
            # Check for Manual Dasa Override
            if birth_details.manual_dasa:
                md = birth_details.manual_dasa
                d_lord = md.get("dasa_lord", "Unknown")
                b_lord = md.get("bhukti_lord", "Unknown")
                a_lord = md.get("antara_lord", "Unknown")
                d_end_str = md.get("dasa_end_date", "Unknown")
                
                # Default "N/A"
                b_end_str = "N/A"
                a_end_str = "N/A"
                d_start_str = "Manual"

                try:
                    # Constants
                    order = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
                    years = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}

                    if d_lord in years and d_end_str != "Unknown":
                        # 1. Back-calculate Dasa Start
                        d_end = datetime.strptime(d_end_str, "%Y-%m-%d")
                        d_duration_days = years[d_lord] * 365.25 # approx
                        d_start = d_end - timedelta(days=d_duration_days)
                        d_start_str = d_start.strftime("%Y-%m-%d")
                        
                        # Recalculate exact total days for fraction logic
                        dasa_total_days = (d_end - d_start).total_seconds() / 86400.0

                        # 2. Find Bhukti End
                        if b_lord in years:
                            # Start from Dasa Start, find matches
                            start_idx = order.index(d_lord)
                            curr = d_start
                            for i in range(9):
                                curr_lord = order[(start_idx + i) % 9]
                                frac = years[curr_lord] / 120.0
                                duration = dasa_total_days * frac
                                end = curr + timedelta(days=duration)
                                if i == 8: end = d_end # Snap to end
                                
                                if curr_lord == b_lord:
                                    b_end_str = end.strftime("%Y-%m-%d")
                                    
                                    # 3. Find Antara End (within this Bhukti)
                                    if a_lord in years:
                                        b_total_days = (end - curr).total_seconds() / 86400.0
                                        b_start_idx = order.index(b_lord)
                                        a_curr = curr
                                        for j in range(9):
                                            a_curr_lord = order[(b_start_idx + j) % 9]
                                            a_frac = years[a_curr_lord] / 120.0
                                            a_duration = b_total_days * a_frac
                                            a_end = a_curr + timedelta(days=a_duration)
                                            if j == 8: a_end = end
                                            
                                            if a_curr_lord == a_lord:
                                                a_end_str = a_end.strftime("%Y-%m-%d")
                                                break
                                            a_curr = a_end
                                    break
                                curr = end
                except Exception as ex:
                    print(f"Manual date calc error: {ex}")

                dasa_info = {
                    "dasa": {"lord": d_lord, "start": d_start_str, "end": d_end_str},
                    "bhukti": {"lord": b_lord, "end": b_end_str},
                    "antara": {"lord": a_lord, "end": a_end_str}
                }
                chart_data['dasa_info'] = dasa_info
                chart_data['dasa_list'] = [] # Not available for manual
            else:
                dasa_list = self.calculate_vimshottari_dasa(birth_details, chart_data)
                dasa_info = self.get_current_dasa_bhukti(dasa_list)
                chart_data['dasa_info'] = dasa_info
                chart_data['dasa_list'] = dasa_list
        except Exception as e:
            print(f"Dasa calculation error: {e}")
            dasa_info = {}
            chart_data['dasa_info'] = {}

        order = ['native_characteristics', 'health', 'career', 'finance', 'stock_market', 'foreign_settlement', 'relationships', 'children', 'education', 'spirituality', 'legal', 'house_property', 'land_real_estate', 'vehicles', 'business_vs_job', 'promotion', 'luck_factor', 'job_change', 'business_start_change', 'dasa_predictions']
        
        if selected_categories:
             order = [c for c in order if c in selected_categories]
             
        predictions = {}
        for c in order:
             if c in cat_map:
                  try:
                       module = cat_map[c]
                       # Handling standard 'analyze' signature across all categories
                       import inspect
                       sig = inspect.signature(module.analyze)
                       if 'dasa_info' in sig.parameters:
                            res = module.analyze(birth_details, chart_data, dasa_info=dasa_info)
                       else:
                            res = module.analyze(birth_details, chart_data)
                                 
                       predictions[c] = res if isinstance(res, dict) else {"points": res, "score": 0}
                  except Exception as e:
                       print(f"Error in {c} analysis: {e}")
                       predictions[c] = {"points": [f"Analysis error: {str(e)}"], "score": 0}
        return predictions

astrology_engine = AstrologyEngine()
