import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "lessons.json")
BANK = os.path.join(ROOT, "data", "vocabulary-bank.json")
now = datetime.now(ZoneInfo("Europe/Berlin"))

# Cron runs at both possible UTC offsets; publish only during Berlin's 08:00 hour.
# A delayed scheduled run within that hour is still accepted.
if now.hour != 8:
    print(f"Not the 08:00 hour in Berlin ({now:%Y-%m-%d %H:%M}); skipping.")
    raise SystemExit(0)

today = now.date().isoformat()
with open(BANK, encoding="utf-8") as f:
    bank = json.load(f)["words"]
with open(DATA, encoding="utf-8") as f:
    data = json.load(f)
if any(item["date"] == today for item in data["lessons"]):
    print(f"Lesson for {today} already exists.")
    raise SystemExit(0)

origin = datetime.fromisoformat("2026-10-14").date()
day_number = max(0, (now.date() - origin).days)
start = (day_number * 25) % len(bank)
chosen = [bank[(start + offset) % len(bank)] for offset in range(25)]
data["lessons"].append({
    "date": today,
    "title": f"Day {day_number + 1} · Daily vocabulary",
    "words": chosen
})
data["lessons"].sort(key=lambda item: item["date"], reverse=True)
with open(DATA, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"Prepared {len(chosen)} words for {today}.")
