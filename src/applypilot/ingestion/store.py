from sqlalchemy.dialects.postgresql import insert
from applypilot.db import SessionLocal
from applypilot.models.job import Job
from typing import cast
from sqlalchemy.engine import CursorResult

def store_jobs(rows: list[dict]) -> int:
    inserted_rowcount: int = 0
    if not rows:
        return 0
    with SessionLocal() as session:
        stmt = insert(Job).values(rows)
        stmt = stmt.on_conflict_do_nothing(index_elements=["source", "external_id"]).returning(Job.id)
        result = session.execute(stmt)
        inserted_rowcount = len(result.fetchall())
        session.commit()
    #print("Inserted rows:", inserted_rowcount)
    return inserted_rowcount