# تقویم شمسی برای آیفون (۱۴۰۵–۱۴۰۶)

| فایل | محتوا |
|---|---|
| `shamsi-date.ics` | تاریخ شمسی هر روز (رویداد تمام‌روز) |
| `iran-holidays.ics` | تعطیلات رسمی؛ ۱۴۰۵ طبق تقویم رسمی، قمری‌های ۱۴۰۶ «تخمینی» |
| `tax-deadlines.ics` | سررسید بیمه، مالیات حقوق، ارزش افزوده و اظهارنامه عملکرد، با یادآور |

## روش ۱: import مستقیم (ساده، بدون به‌روزرسانی)
فایل را به آیفون بفرستید (ایمیل، تلگرام، Files) ← روی آن بزنید ← **Add All**.

## روش ۲: اشتراک (لینک دائمی، خودکار به‌روز می‌شود)
آیفون: **Settings ← Calendar ← Accounts ← Add Account ← Other ← Add Subscribed Calendar** و یکی از این لینک‌ها:

- تاریخ شمسی: `https://raw.githubusercontent.com/mohammadrezavakilzadeh-code/shamsi-calendar/main/shamsi-date.ics`
- تعطیلات: `https://raw.githubusercontent.com/mohammadrezavakilzadeh-code/shamsi-calendar/main/iran-holidays.ics`
- سررسیدها: `https://raw.githubusercontent.com/mohammadrezavakilzadeh-code/shamsi-calendar/main/tax-deadlines.ics`

> برای سررسیدها، هنگام اشتراک گزینه **Remove Alerts** را خاموش کنید تا یادآورها بمانند.

## به‌روزرسانی
وقتی تقویم رسمی ۱۴۰۶ منتشر شد (معمولاً آبان/آذر)، تاریخ‌های قمری ۱۴۰۶ در `build.py` را اصلاح و فایل‌ها را دوباره بسازید: `python3 build.py`
