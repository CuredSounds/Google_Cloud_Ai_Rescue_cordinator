from typing import List
from app.models import Scenario, Survivor, Mission
from app.config import settings
import vertexai
from vertexai.generative_models import GenerativeModel
import json
import uuid

class Coordinator:
    def __init__(self):
        try:
            vertexai.init(project=settings.PROJECT_ID, location=settings.REGION)
            self.model = GenerativeModel("gemini-1.5-pro-preview-0409")
        except Exception:
            self.model = None

    async def assign_team(self, scenario: Scenario, survivors: List[Survivor]) -> Mission:
        if not self.model:
            return self._assign_team_mock(scenario, survivors)

        # Convert survivors to a simplified string format for the prompt
        survivor_list_str = "\n".join([
            f"- {s.id}: {s.name} (Role: {s.role}, Skills: {s.skills}, XP: {s.xp_points}, Status: {s.status})"
            for s in survivors if s.status == "On-Call"
        ])

        prompt = f"""
        You are the Rescue Coordinator. A crisis has occurred.
        
        Scenario: {scenario.title}
        Description: {scenario.description}
        Severity: {scenario.severity}
        Required Skills: {scenario.required_skills}

        Available Personnel:
        {survivor_list_str}

        Task: Select a team of 3 survivors to handle this crisis. 
        Balance skill requirements with the need to train junior members (low XP).
        
        Return a JSON object with:
        - reason: Brief explanation of your choice.
        - assigned_ids: List of 3 Survivor IDs.
        """

        try:
            response = await self.model.generate_content_async(prompt)
            text = response.text.replace("```json", "").replace("```", "")
            data = json.loads(text)
            
            return Mission(
                id=str(uuid.uuid4()),
                scenario_id=scenario.id,
                assigned_team=data["assigned_ids"]
            )
        except Exception as e:
            print(f"Error assigning team: {e}")
            return self._assign_team_mock(scenario, survivors)

    def _assign_team_mock(self, scenario: Scenario, survivors: List[Survivor]) -> Mission:
        # Simple random assignment of available personnel
        available = [s.id for s in survivors if s.status == "On-Call"]
        assigned = available[:3] if len(available) >= 3 else available
        return Mission(
            id=str(uuid.uuid4()),
            scenario_id=scenario.id,
            assigned_team=assigned
        )
