import httpx
from applypilot.config import settings

def fetch_adzuna_jobs(what: str, where: str | None = None, page: int = 1, max_days_old: int = 30) -> list[dict]:
    url = f"https://api.adzuna.com/v1/api/jobs/us/search/{page}"
    params = {
        "app_id": settings.adzuna_app_id,
        "app_key": settings.adzuna_app_key,
        "what": what,
        "max_days_old": max_days_old,
        "results_per_page": 10,
    }
    if where:
        params["where"] = where
    response = httpx.get(url, params=params, timeout=30)
    response.raise_for_status()            
    return response.json()["results"]
