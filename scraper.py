import requests
from typing import List, Optional
from schemas import TrialCreate

# API Endpoint for ClinicalTrials v2 JSON API
API_URL = "https://clinicaltrials.gov/api/v2/studies"

def fetch_trials(page_size: int = 20, date_filter: Optional[str] = None) -> List[TrialCreate]:
    """
    Fetches trial data from clinicaltrials.gov and parses it into a list of TrialCreate schemas.
    """
    params = {
        "pageSize": page_size,
    }
    if date_filter:
        # Assuming date_filter is a single date string like "2024-07-15"
        # Using LastUpdateSubmitDate because that's the field we store in the DB
        params["filter.advanced"] = f"AREA[LastUpdateSubmitDate]RANGE[{date_filter}, {date_filter}]"
        
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    
    data = response.json()
    studies = data.get("studies", [])
    
    parsed_trials = []
    
    for study in studies:
        protocol_section = study.get("protocolSection", {})
        
        # Identification
        ident_module = protocol_section.get("identificationModule", {})
        nct_id = ident_module.get("nctId")
        title = ident_module.get("briefTitle") or ident_module.get("officialTitle")
        
        # Status
        status_module = protocol_section.get("statusModule", {})
        status = status_module.get("overallStatus")
        last_update = status_module.get("lastUpdateSubmitDate")
        
        # Conditions
        conditions_module = protocol_section.get("conditionsModule", {})
        conditions_list = conditions_module.get("conditions", [])
        conditions_str = ", ".join(conditions_list) if conditions_list else None
        
        # Interventions
        interventions_module = protocol_section.get("armsInterventionsModule", {})
        interventions_list = interventions_module.get("interventions", [])
        intervention_names = [inv.get("name") for inv in interventions_list if inv.get("name")]
        interventions_str = ", ".join(intervention_names) if intervention_names else None
        
        if nct_id:
            trial = TrialCreate(
                nct_id=nct_id,
                title=title,
                status=status,
                conditions=conditions_str,
                interventions=interventions_str,
                last_update_submitted=last_update
            )
            parsed_trials.append(trial)
            
    return parsed_trials
