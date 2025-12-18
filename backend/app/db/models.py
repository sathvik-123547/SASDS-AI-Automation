import datetime as dt

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class RunLog(Base):
    __tablename__ = "run_logs"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)
    run_id = Column(String, index=True, nullable=True)
    kind = Column(String, nullable=False)  # e.g. analysis|codegen|tests|review|write
    payload = Column(Text, nullable=False)  # JSON string
    note = Column(String, nullable=True)


