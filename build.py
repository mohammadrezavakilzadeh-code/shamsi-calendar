"""Build three .ics calendars for 1405-1406: official holidays, tax/insurance deadlines, daily Shamsi date."""
import jdatetime, uuid, hashlib
from datetime import date, timedelta, datetime, timezone
from hijridate import Hijri, Gregorian

FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
MONTHS = ["فروردین","اردیبهشت","خرداد","تیر","مرداد","شهریور","مهر","آبان","آذر","دی","بهمن","اسفند"]
WEEK = ["دوشنبه","سه‌شنبه","چهارشنبه","پنجشنبه","جمعه","شنبه","یکشنبه"]  # python weekday 0=Mon

def j(y, m, d): return jdatetime.date(y, m, d).togregorian()
def fa(n): return str(n).translate(FA)
def jstr(g):
    jd = jdatetime.date.fromgregorian(date=g)
    return f"{WEEK[g.weekday()]} {fa(jd.day)} {MONTHS[jd.month-1]} {fa(jd.year)}"

# ---------- 1405: official calendar (شورای فرهنگ عمومی) as published ----------
H1405 = [
    ((1405,1,1),"آغاز نوروز / عید سعید فطر"),
    ((1405,1,2),"عید نوروز / تعطیل به مناسبت عید فطر"),
    ((1405,1,3),"عید نوروز"),
    ((1405,1,4),"عید نوروز"),
    ((1405,1,12),"روز جمهوری اسلامی"),
    ((1405,1,13),"روز طبیعت"),
    ((1405,1,25),"شهادت امام جعفر صادق (ع)"),
    ((1405,3,6),"عید سعید قربان"),
    ((1405,3,14),"عید غدیر خم / رحلت امام خمینی"),
    ((1405,3,15),"قیام ۱۵ خرداد"),
    ((1405,4,3),"تاسوعای حسینی"),
    ((1405,4,4),"عاشورای حسینی"),
    ((1405,5,13),"اربعین حسینی"),
    ((1405,5,21),"رحلت پیامبر اکرم (ص) و شهادت امام حسن مجتبی (ع)"),
    ((1405,5,22),"شهادت امام رضا (ع)"),
    ((1405,5,30),"شهادت امام حسن عسکری (ع)"),
    ((1405,6,8),"ولادت پیامبر اکرم (ص) و امام جعفر صادق (ع)"),
    ((1405,8,22),"شهادت حضرت فاطمه زهرا (س)"),
    ((1405,10,2),"ولادت امام علی (ع) / روز پدر"),
    ((1405,10,16),"مبعث حضرت رسول اکرم (ص)"),
    ((1405,11,4),"ولادت حضرت قائم (عج) / نیمه شعبان"),
    ((1405,11,22),"پیروزی انقلاب اسلامی"),
    ((1405,12,9),"شهادت امام علی (ع)"),
    ((1405,12,19),"عید سعید فطر"),
    ((1405,12,20),"تعطیل به مناسبت عید فطر"),
    ((1405,12,29),"روز ملی شدن صنعت نفت"),
]

# ---------- 1406: official calendar not yet published -> solar fixed + lunar estimated ----------
START_1406, END_1406 = j(1406,1,1), j(1406,12,29)
SOLAR_1406 = [((1406,1,1),"آغاز نوروز"),((1406,1,2),"عید نوروز"),((1406,1,3),"عید نوروز"),((1406,1,4),"عید نوروز"),
              ((1406,1,12),"روز جمهوری اسلامی"),((1406,1,13),"روز طبیعت"),((1406,3,14),"رحلت امام خمینی"),
              ((1406,3,15),"قیام ۱۵ خرداد"),((1406,11,22),"پیروزی انقلاب اسلامی"),((1406,12,29),"روز ملی شدن صنعت نفت")]
LUNAR = [((1,9),"تاسوعای حسینی"),((1,10),"عاشورای حسینی"),((2,20),"اربعین حسینی"),
         ((2,28),"رحلت پیامبر اکرم (ص) و شهادت امام حسن مجتبی (ع)"),("ENDSAFAR","شهادت امام رضا (ع)"),
         ((3,8),"شهادت امام حسن عسکری (ع)"),((3,17),"ولادت پیامبر اکرم (ص) و امام جعفر صادق (ع)"),
         ((6,3),"شهادت حضرت فاطمه زهرا (س)"),((7,13),"ولادت امام علی (ع) / روز پدر"),((7,27),"مبعث حضرت رسول اکرم (ص)"),
         ((8,15),"ولادت حضرت قائم (عج) / نیمه شعبان"),((9,21),"شهادت امام علی (ع)"),((10,1),"عید سعید فطر"),
         ((10,2),"تعطیل به مناسبت عید فطر"),((10,25),"شهادت امام جعفر صادق (ع)"),((12,10),"عید سعید قربان"),((12,18),"عید غدیر خم")]
OFFSET = 1  # Iran's official lunar dates in 1405 ran mostly +1 day vs Umm al-Qura tables

def h2g(y, m, d):
    g = Hijri(y, m, d).to_gregorian(); return date(g.year, g.month, g.day) + timedelta(days=OFFSET)

def lunar_1406():
    out = []
    for hy in (1448, 1449):
        for key, name in LUNAR:
            if key == "ENDSAFAR":
                g = h2g(hy, 3, 1) - timedelta(days=1)
            else:
                g = h2g(hy, *key)
            if START_1406 <= g <= END_1406:
                out.append((g, name))
    return out

holidays = [(j(*d), n, False) for d, n in H1405]
holidays += [(j(*d), n, False) for d, n in SOLAR_1406]
holidays += [(g, n, True) for g, n in lunar_1406()]
holidays.sort()
HOLIDAY_SET = {g for g, _, _ in holidays} | {j(1407,1,d) for d in (1,2,3,4,12,13)}

def next_workday(g):
    moved = False
    while g.weekday() == 4 or g in HOLIDAY_SET:  # Friday or official holiday
        g += timedelta(days=1); moved = True
    return g, moved

# ---------- ICS helpers ----------
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
def esc(s): return s.replace("\\","\\\\").replace(";","\\;").replace(",","\\,").replace("\n","\\n")
def fold(line):
    b = line.encode(); out = []
    while len(b) > 73:
        cut = 73
        while (b[cut] & 0xC0) == 0x80: cut -= 1
        out.append(b[:cut].decode()); b = b[cut:]
    out.append(b.decode()); return "\r\n ".join(out)

def calendar(name, color, events):
    L = ["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//Shamsi Calendar 1405-1406//FA","CALSCALE:GREGORIAN","METHOD:PUBLISH",
         f"X-WR-CALNAME:{esc(name)}","X-WR-TIMEZONE:Asia/Tehran",f"X-APPLE-CALENDAR-COLOR:{color}",
         "REFRESH-INTERVAL;VALUE=DURATION:P1D","X-PUBLISHED-TTL:P1D"]
    for e in events:
        uid = hashlib.md5((name + e["date"].isoformat() + e["title"]).encode()).hexdigest() + "@shamsi-cal"
        L += ["BEGIN:VEVENT", f"UID:{uid}", f"DTSTAMP:{STAMP}",
              f"DTSTART;VALUE=DATE:{e['date']:%Y%m%d}", f"DTEND;VALUE=DATE:{e['date']+timedelta(days=1):%Y%m%d}",
              f"SUMMARY:{esc(e['title'])}", "TRANSP:TRANSPARENT"]
        if e.get("desc"): L.append(f"DESCRIPTION:{esc(e['desc'])}")
        for days in e.get("alarms", []):
            # all-day event starts 00:00 → alarm at 09:00 local N days before
            trig = f"-P{days-1}DT15H" if days else "PT9H"
            L += ["BEGIN:VALARM","ACTION:DISPLAY",f"DESCRIPTION:{esc(e['title'])}",f"TRIGGER:{trig}","END:VALARM"]
        L.append("END:VEVENT")
    L.append("END:VCALENDAR")
    return "\r\n".join(fold(x) for x in L) + "\r\n"

# ---------- 1) holidays ----------
hol_events = []
for g, n, est in holidays:
    title = f"🔴 {n}" + (" (تخمینی)" if est else "")
    desc = jstr(g) + ("\nتقویم رسمی ۱۴۰۶ هنوز منتشر نشده؛ تعطیلات قمری با محاسبه نجومی تخمین زده شده و ممکن است ±۱ روز جابه‌جا شود." if est else "\nمنبع: تقویم رسمی ۱۴۰۵ (شورای فرهنگ عمومی)")
    hol_events.append({"date": g, "title": title, "desc": desc})

# ---------- 2) deadlines (from Mehr 1405 through 1406) ----------
dl = []
def add(gdate, title, desc, alarms=(3, 0)):
    real, moved = next_workday(gdate)
    d = desc + f"\nمهلت تقویمی: {jstr(gdate)}"
    if moved:
        d += f"\nچون آخرین روز مهلت تعطیل است، به اولین روز کاری بعد منتقل شد: {jstr(real)}"
    dl.append({"date": real, "title": title, "desc": d, "alarms": list(alarms)})

def last_day(y, m):
    return 31 if m <= 6 else (30 if m <= 11 else (30 if jdatetime.date(y,1,1).isleap() else 29))

# monthly: insurance list + payroll tax for month M due end of M+1
months = [(1405, m) for m in range(6, 13)] + [(1406, m) for m in range(1, 12)]
for y, m in months:
    ny, nm = (y, m + 1) if m < 12 else (y + 1, 1)
    add(j(ny, nm, last_day(ny, nm)),
        f"📌 لیست بیمه و مالیات حقوق {MONTHS[m-1]} {fa(y)}",
        "ارسال لیست و پرداخت حق بیمه تأمین اجتماعی (ماده ۳۹ قانون تأمین اجتماعی)\n"
        "+ ارسال فهرست و پرداخت مالیات تکلیفی حقوق (ماده ۸۶ ق.م.م)")

# VAT: legal deadline 15th of month after quarter
vat = [((1405,7,15),"تابستان ۱۴۰۵"),((1405,10,15),"پاییز ۱۴۰۵"),((1406,1,15),"زمستان ۱۴۰۵"),
       ((1406,4,15),"بهار ۱۴۰۶"),((1406,7,15),"تابستان ۱۴۰۶"),((1406,10,15),"پاییز ۱۴۰۶")]
for d, q in vat:
    if j(*d) < date(2026, 10, 7): continue
    add(j(*d), f"📌 اظهارنامه ارزش افزوده {q}",
        "مهلت قانونی ارسال اظهارنامه و پرداخت مالیات بر ارزش افزوده (۱۵ روز پس از پایان دوره).\n"
        "سازمان امور مالیاتی معمولاً به‌خاطر مهلت ۳۰ روزه واکنش خریدار در سامانه مؤدیان تمدید می‌کند؛ بخشنامه تمدید را در intamedia.ir چک کنید.",
        alarms=(7, 3, 0))

add(j(1406,3,31), "📌 اظهارنامه عملکرد اشخاص حقیقی و اجاره ۱۴۰۵",
    "مهلت تسلیم اظهارنامه مالیاتی مشاغل و درآمد اجاره سال ۱۴۰۵ و پرداخت مالیات", alarms=(14, 7, 3, 0))
add(j(1406,4,31), "📌 اظهارنامه عملکرد اشخاص حقوقی ۱۴۰۵",
    "مهلت تسلیم اظهارنامه، ترازنامه و حساب سود و زیان سال مالی منتهی به ۲۹ اسفند ۱۴۰۵ (ماده ۱۱۰ ق.م.م) و پرداخت مالیات.\n"
    "همچنین سقف برگزاری مجمع عمومی عادی سالانه: ۴ ماه پس از پایان سال مالی.", alarms=(30, 14, 7, 3, 0))
dl.sort(key=lambda e: e["date"])

# ---------- 3) daily Shamsi date ----------
daily = []
g = j(1405,1,1)
while g <= END_1406:
    jd = jdatetime.date.fromgregorian(date=g)
    daily.append({"date": g, "title": f"{fa(jd.day)} {MONTHS[jd.month-1]} {fa(jd.year)}"})
    g += timedelta(days=1)

open("iran-holidays.ics","w",newline="").write(calendar("تعطیلات رسمی ایران ۱۴۰۵-۱۴۰۶","#E53935",hol_events))
open("tax-deadlines.ics","w",newline="").write(calendar("سررسیدهای مالیات و بیمه","#1E88E5",dl))
open("shamsi-date.ics","w",newline="").write(calendar("تاریخ شمسی","#43A047",daily))

print(len(hol_events), len(dl), len(daily))
for g, n, est in holidays:
    if g >= START_1406: print(jstr(g), n, "EST" if est else "")
print("----")
for e in dl: print(jstr(e["date"]), e["title"])
