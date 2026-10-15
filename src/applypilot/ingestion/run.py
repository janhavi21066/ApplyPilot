import httpx
import time

from applypilot.ingestion.store import store_jobs
from applypilot.ingestion.adzuna import fetch_adzuna_jobs
from applypilot.ingestion.normalize import normalize_adzuna

SEARCHES = [
    ("software engineer", "Dallas, TX"),
    ("software engineering intern", "Dallas, TX"),
    ("machine learning engineer", "Dallas, TX"),
    ("remote software engineer", None),
    ("remote machine learning engineer", None),
    ("forward deployed engineer", "Dallas, TX"),
]
PAGES_PER_SEARCH = 3

def main():
    for what, where in SEARCHES:
        skipped = 0
        inserted = 0
        raw_jobs = []
        rows = []
        for page in range(1, PAGES_PER_SEARCH + 1):
            time.sleep(3)
            try:
                page_jobs = fetch_adzuna_jobs(what, where, page=page)
                if not page_jobs:
                    print(f"No jobs found for {what!r} / {where!r} on page {page}")
                    break
                raw_jobs.extend(page_jobs)
            except httpx.HTTPError as e:
                print(f"Fetch failed for {what!r} / {where!r}: {e}")
                break
        fetched = len(raw_jobs)
        for raw_job in raw_jobs:
            normalized = normalize_adzuna(raw_job)
            if normalized is None:
                skipped += 1
                continue
            rows.append(normalized)
        inserted = store_jobs(rows)
        print(f"what: {what}, where: {where}, fetched: {fetched}, inserted: {inserted}, skipped: {skipped}")  
if __name__ == "__main__":
    main()
