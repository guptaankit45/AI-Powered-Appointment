from dateparser.search import search_dates
from datetime import datetime
from zoneinfo import ZoneInfo

def normalize_entities(entities: dict) -> dict:
    department = entities.get("department")
    raw_text = entities.get("raw_text") or ""

    if not department:
        return {"status": "needs_clarification", "message": "Department not found in input."}

    # Prefer future dates, resolve relative phrases from IST "now", and return tz-aware datetimes
    settings = {
        "PREFER_DATES_FROM": "future",
        "RELATIVE_BASE": datetime.now(ZoneInfo("Asia/Kolkata")),
        "TIMEZONE": "Asia/Kolkata",
        "RETURN_AS_TIMEZONE_AWARE": True,
    }

    candidates = search_dates(raw_text, settings=settings) or []

    # Choose the first candidate that includes a time (hour/minute not zero), else fall back to first date-only
    best_dt = None
    for span, dt in candidates:
        if dt and (dt.hour != 0 or dt.minute != 0):
            best_dt = dt
            break
    if not best_dt and candidates:
        best_dt = candidates[0][1]

    if not best_dt:
        return {"status": "needs_clarification", "message": "Date/time not found or ambiguous."}

    return {
        "appointment": {
            "department": department,
            "date": best_dt.date().isoformat(),
            "time": best_dt.time().strftime("%H:%M"),
            "timezone": "Asia/Kolkata",
        },
        "status": "ok",
    }
