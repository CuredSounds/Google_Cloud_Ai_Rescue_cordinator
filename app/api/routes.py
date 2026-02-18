from fastapi import APIRouter, HTTPException
from app.simulation.world_engine import WorldEngine
from app.agents.coordinator import Coordinator
from app.simulation.mission_sim import MissionSim
from app.simulation.evaluator import Evaluator
from app.database import save_scenario, get_all_survivors, save_mission, get_scenario, get_mission
from app.models import Scenario, Mission

router = APIRouter()

world_engine = WorldEngine()
coordinator = Coordinator()
mission_sim = MissionSim()
evaluator = Evaluator()

@router.post("/scenario/generate", response_model=Scenario)
async def generate_scenario():
    scenario = await world_engine.generate_scenario()
    save_scenario(scenario)
    return scenario

@router.post("/mission/assign/{scenario_id}", response_model=Mission)
async def assign_team(scenario_id: str):
    scenario = get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    survivors = get_all_survivors()
    mission = await coordinator.assign_team(scenario, survivors)
    save_mission(mission)
    return mission

@router.post("/mission/run/{mission_id}", response_model=Mission)
async def run_mission(mission_id: str):
    mission = get_mission(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    scenario = get_scenario(mission.scenario_id)
    # Reconstruct team objects from IDs
    team = [s for s in get_all_survivors() if s.id in mission.assigned_team]
    
    mission = await mission_sim.run_mission(mission, scenario, team)
    return mission

@router.post("/mission/evaluate/{mission_id}", response_model=Mission)
async def evaluate_mission(mission_id: str):
    mission = get_mission(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    scenario = get_scenario(mission.scenario_id)
    mission = await evaluator.evaluate_mission(mission, scenario)
    return mission

@router.post("/simulation/full_loop", response_model=Mission)
async def run_full_loop():
    # 1. Generate Scenario
    scenario = await world_engine.generate_scenario()
    save_scenario(scenario)
    
    # 2. Assign Team
    survivors = get_all_survivors()
    mission = await coordinator.assign_team(scenario, survivors)
    save_mission(mission)
    
    # 3. Run Mission
    team = [s for s in get_all_survivors() if s.id in mission.assigned_team]
    mission = await mission_sim.run_mission(mission, scenario, team)
    
    # 4. Evaluate
    mission = await evaluator.evaluate_mission(mission, scenario)
    
    return mission
