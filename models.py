from sqlalchemy import Column, String, Text, DateTime
from database import Base
import datetime

class Trial(Base):
    __tablename__ = "clinical_trials"

    nct_id = Column(String(50), primary_key=True, index=True)
    title = Column(Text, nullable=True)
    status = Column(String(100), nullable=True)
    conditions = Column(Text, nullable=True)
    interventions = Column(Text, nullable=True)
    last_update_submitted = Column(String(50), nullable=True)
    fetched_at = Column(DateTime, default=datetime.datetime.utcnow)
