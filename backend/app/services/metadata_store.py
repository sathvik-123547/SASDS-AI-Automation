import json
import uuid
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, engine
from app.db import models

# Ensure tables exist
models.Base.metadata.create_all(bind=engine)


def _serialize_payload(data) -> str:
    if isinstance(data, str):
        return data
    return json.dumps(data, default=str)


def log_event(kind: str, payload, run_id: Optional[str] = None, note: Optional[str] = None) -> str:
    """
    Persist a log entry. Returns the run_id used for grouping.
    """
    run_id = run_id or f"run_{uuid.uuid4().hex[:8]}"
    db: Session = SessionLocal()
    try:
        entry = models.RunLog(
            run_id=run_id,
            kind=kind,
            payload=_serialize_payload(payload),
            note=note,
        )
        db.add(entry)
        db.commit()
        return run_id
    except SQLAlchemyError:
        db.rollback()
        # Fail soft; do not break main flow
        return run_id
    finally:
        db.close()


