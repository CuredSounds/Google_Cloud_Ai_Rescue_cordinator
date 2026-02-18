from app.models import Scenario, Mission, Survivor
from typing import List
import vertexai
from vertexai.generative_models import GenerativeModel
from app.config import settings

class MissionSim:
    def __init__(self):
        try:
            vertexai.init(project=settings.PROJECT_ID, location=settings.REGION)
            self.model = GenerativeModel("gemini-1.5-flash-preview-0514") # Use Flash for speed
        except Exception:
            self.model = None

    async def run_mission(self, mission: Mission, scenario: Scenario, team: List[Survivor]) -> Mission:
        if not self.model:
            return self._run_mock_mission(mission, scenario, team)

        team_desc = "\n".join([f"{s.name} ({s.role}, Skills: {s.skills})" for s in team])
        
        prompt = f"""
        Simulate a rescue mission.
        
        Scenario: {scenario.title}
        Description: {scenario.description}
        Severity: {scenario.severity}
        
        The Team:
        {team_desc}
        
        Simulate a short dialogue (3-5 turns) where the team discusses the problem and attempts to solve it.
        Focus on how their skills are applied.
        
        Output the dialogue as a list of strings, e.g., "Commander X: We need to breach the door."
        """

        try:
            response = await self.model.generate_content_async(prompt)
            # Naive splitting by line
            mission.log = response.text.strip().split("\n")
            return mission
        except Exception as e:
            print(f"Error running mission: {e}")
            return self._run_mock_mission(mission, scenario, team)

    def _run_mock_mission(self, mission: Mission, scenario: Scenario, team: List[Survivor]) -> Mission:
        mission.log = [
            f"{team[0].name}: Assessing the situation.",
            f"{team[1].name}: I can use my {list(team[1].skills.keys())[0]} skill here.",
            f"{team[0].name}: Proceeding with the plan.",
            "System: The team successfully neutralized the threat."
        ]
        return mission
