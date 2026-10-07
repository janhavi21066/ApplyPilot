import httpx

from applypilot.ingestion.store import store_jobs
from applypilot.ingestion.adzuna import fetch_adzuna_jobs
from applypilot.ingestion.normalize import normalize_adzuna

import time

SEARCHES = [
    ("software engineer", "Dallas, TX"),
    ("software engineering intern", "Dallas, TX"),
    ("machine learning engineer", "Dallas, TX"),
    ("remote software engineer", None),
    ("remote machine learning engineer", None),
    ("forward deployed engineer", "Dallas, TX"),
]
def main():
    skipped = 0
    fetched = 0
    for what, where in SEARCHES:
        time.sleep(3)
        skipped = 0
        rows = []
        try:
            raw_jobs = fetch_adzuna_jobs(what, where)
        except httpx.HTTPError as e:
            print(f"Fetch failed for {what!r} / {where!r}: {e}")
            continue
        fetched = len(raw_jobs)
        for raw_job in raw_jobs:
            normalized = normalize_adzuna(raw_job)
            if normalized is None:
                skipped += 1
                continue
            rows.append(normalized)
        inserted = store_jobs(rows)
        print(f"what: {what}, where: {where}, fetched: {fetched} inserted: {inserted}, skipped: {skipped}")  
if __name__ == "__main__":
    main()
