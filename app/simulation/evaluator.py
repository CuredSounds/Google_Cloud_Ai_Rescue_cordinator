from app.models import Mission, Scenario
import vertexai
from vertexai.generative_models import GenerativeModel
from app.config import settings
import json

class Evaluator:
    def __init__(self):
        try:
            vertexai.init(project=settings.PROJECT_ID, location=settings.REGION)
            self.model = GenerativeModel("gemini-1.5-flash-preview-0514")
        except Exception:
            self.model = None

    async def evaluate_mission(self, mission: Mission, scenario: Scenario) -> Mission:
        if not self.model:
            return self._mock_evaluate(mission)

        log_str = "\n".join(mission.log)
        
        prompt = f"""
        Evaluate this mission log.
        
        Scenario: {scenario.title} (Severity: {scenario.severity})
        Log:
        {log_str}
        
        Did they succeed? How much XP should be awarded (1-100)?
        
        Return JSON:
        - outcome: "Success" or "Failure"
        - xp: Integer
        """

        try:
            response = await self.model.generate_content_async(prompt)
            text = response.text.replace("```json", "").replace("```", "")
            data = json.loads(text)
            
            mission.outcome = data["outcome"]
            mission.xp_awarded = data["xp"]
            return mission
        except Exception as e:
            print(f"Error evaluating: {e}")
            return self._mock_evaluate(mission)

    def _mock_evaluate(self, mission: Mission) -> Mission:
        mission.outcome = "Success"
        mission.xp_awarded = 50
        return mission
