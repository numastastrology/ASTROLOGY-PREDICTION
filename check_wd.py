import swisseph as swe
from datetime import datetime

t = datetime(2009, 4, 9) # Thursday
jd = swe.julday(2009, 4, 9, 12)
wd = swe.day_of_week(jd)
print(f"2009-04-09 (Thursday) JD: {jd} WD: {wd}")

t2 = datetime(2009, 4, 5) # Sunday
jd2 = swe.julday(2009, 4, 5, 12)
wd2 = swe.day_of_week(jd2)
print(f"2009-04-05 (Sunday) JD: {jd2} WD: {wd2}")
