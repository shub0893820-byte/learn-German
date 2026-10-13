import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "lessons.json")
BANK = os.path.join(ROOT, "data", "vocabulary-bank.json")
now = datetime.now(ZoneInfo("Europe/Berlin"))

# Scheduled runs use both UTC offsets for Berlin daylight-saving time.
# Allow manual workflow_dispatch runs at any time so the workflow can be tested.
event = os.environ.get("GITHUB_EVENT_NAME", "schedule")
if event != "workflow_dispatch" and now.hour != 8:
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
start = (day_number * 10) % len(bank)
chosen = [bank[(start + offset) % len(bank)] for offset in range(10)]
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
