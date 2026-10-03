from datetime import datetime
from applypilot.models.job import WorkMode

def normalize_adzuna(raw: dict) -> dict | None:
    normalized = {
        "source": "adzuna",
        "external_id": raw.get("id"),
        "title": (raw.get("title") or None),
        "company": ((raw.get("company") or {}).get("display_name") or None),
        "location": (raw.get("location") or {}).get("display_name"),
        "description": raw.get("description"),
        "url": raw.get("redirect_url"),
        "posted_at": None,
        "raw_data": raw,
        "work_mode": None,
    }
    if not normalized["external_id"] or not normalized["title"] or not normalized["company"]:
        return None
    if raw.get("created"):
        normalized["posted_at"] = datetime.fromisoformat(raw["created"])
    normalized["work_mode"] = normalize_work_mode(raw)
    return normalized

def normalize_work_mode(raw: dict) -> WorkMode | None:
    title = raw.get("title") or ""
    description = raw.get("description") or ""
    work_mode_identifier: str = (title + " " + description).lower()
    if "hybrid" in work_mode_identifier:
        return WorkMode.HYBRID
    elif "onsite" in work_mode_identifier or "on-site" in work_mode_identifier:
        return WorkMode.ONSITE
    elif "remote" in work_mode_identifier:
        return WorkMode.REMOTE
    else:
        return None
