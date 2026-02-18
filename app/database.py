from typing import Dict, List
from app.models import Survivor, Scenario, Mission
import uuid

# Mock Data
SURVIVORS: Dict[str, Survivor] = {}
SCENARIOS: Dict[str, Scenario] = {}
MISSIONS: Dict[str, Mission] = {}

def init_db():
    print("Initializing Mock Database...")
    # Add some mock survivors
    roles = ["Firefighter", "Medic", "Engineer", "Scout", "Commander"]
    names = ["Alex", "Sam", "Jordan", "Casey", "Morgan", "Riley", "Quinn"]
    
    for i, name in enumerate(names):
        s_id = str(uuid.uuid4())
        role = roles[i % len(roles)]
        SURVIVORS[s_id] = Survivor(
            id=s_id,
            name=name,
            role=role,
            skills={role: 3, "Leadership": 1},
            status="On-Call"
        )
    print(f"Added {len(SURVIVORS)} survivors.")

def get_all_survivors() -> List[Survivor]:
    return list(SURVIVORS.values())

def get_survivor(id: str) -> Survivor:
    return SURVIVORS.get(id)

def save_scenario(scenario: Scenario):
    SCENARIOS[scenario.id] = scenario

def get_scenario(id: str) -> Scenario:
    return SCENARIOS.get(id)

def save_mission(mission: Mission):
    MISSIONS[mission.id] = mission

def get_mission(id: str) -> Mission:
    return MISSIONS.get(id)
