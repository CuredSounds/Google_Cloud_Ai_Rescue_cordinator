from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class Survivor(BaseModel):
    id: str
    name: str
    role: str
    status: Literal["On-Call", "Deployed", "Resting"] = "On-Call"
    traits: List[str] = []
    xp_points: int = 0
    skills: dict[str, int] = {} # e.g., {"First Aid": 3, "Leadership": 1}

class Scenario(BaseModel):
    id: str
    title: str
    description: str
    severity: int = Field(..., ge=1, le=5) # 1 to 5 scale
    location: str
    required_skills: List[str]
    status: Literal["Active", "Resolved", "Failed"] = "Active"

class Mission(BaseModel):
    id: str
    scenario_id: str
    assigned_team: List[str] # List of Survivor IDs
    log: List[str] = []
    outcome: Optional[Literal["Success", "Failure"]] = None
    xp_awarded: int = 0
