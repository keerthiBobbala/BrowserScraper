from pydantic import BaseModel
from typing import Optional

class TrialBase(BaseModel):
    nct_id: str
    title: Optional[str] = None
    status: Optional[str] = None
    conditions: Optional[str] = None
    interventions: Optional[str] = None
    last_update_submitted: Optional[str] = None

class TrialCreate(TrialBase):
    pass

class TrialResponse(TrialBase):
    class Config:
        from_attributes = True
