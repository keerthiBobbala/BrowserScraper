from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
from database import engine, get_db
from scraper import fetch_trials

# Create the database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Clinical Trials Scraper API",
    description="API to fetch data from clinicaltrials.gov and store it in SQL Server",
    version="1.0.0"
)

@app.post("/fetch-trials", response_model=List[schemas.TrialResponse])
def trigger_fetch_and_store(page_size: int = 20, date_filter: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Fetches trials from clinicaltrials.gov and stores them in the database.
    Updates existing trials if they already exist based on nct_id.
    """
    try:
        # 1. Fetch data
        trials_data = fetch_trials(page_size=page_size, date_filter=date_filter)
        
        # 2. Store data
        stored_trials = []
        for trial_in in trials_data:
            # Check if trial already exists
            existing_trial = db.query(models.Trial).filter(models.Trial.nct_id == trial_in.nct_id).first()
            
            if existing_trial:
                # Update fields
                for key, value in trial_in.dict().items():
                    setattr(existing_trial, key, value)
                stored_trials.append(existing_trial)
            else:
                # Create new
                new_trial = models.Trial(**trial_in.dict())
                db.add(new_trial)
                stored_trials.append(new_trial)
                
        db.commit()
        
        # Refresh to get updated data
        for trial in stored_trials:
            db.refresh(trial)
            
        return stored_trials
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trials", response_model=List[schemas.TrialResponse])
def get_stored_trials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves the clinical trials currently stored in the database.
    """
    trials = db.query(models.Trial).order_by(models.Trial.nct_id).offset(skip).limit(limit).all()
    return trials
