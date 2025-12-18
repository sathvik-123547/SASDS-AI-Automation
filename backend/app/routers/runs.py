from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models import RunLog
from app.db.session import SessionLocal

router = APIRouter(
    prefix="/runs",
    tags=["Runs"],
)


def get_db():
  db = SessionLocal()
  try:
      yield db
  finally:
      db.close()


@router.get("/")
def list_runs(limit: int = 50, db: Session = Depends(get_db)):
    """
    Return recent run log entries (without huge payloads by default).
    """
    q = (
        db.query(RunLog)
        .order_by(RunLog.created_at.desc())
        .limit(limit)
    )
    items = [
        {
            "id": r.id,
            "created_at": r.created_at.isoformat(),
            "run_id": r.run_id,
            "kind": r.kind,
            "note": r.note,
        }
        for r in q
    ]
    return {"runs": items}



