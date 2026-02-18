import vertexai
from vertexai.generative_models import GenerativeModel, Part
import json
from app.models import Scenario
from app.config import settings
import uuid

class WorldEngine:
    def __init__(self):
        # Initialize Vertex AI
        try:
            vertexai.init(project=settings.PROJECT_ID, location=settings.REGION)
            self.model = GenerativeModel("gemini-1.5-pro-preview-0409") # Or latest available
        except Exception as e:
            print(f"Warning: Vertex AI init failed. Using mock mode. Error: {e}")
            self.model = None

    async def generate_scenario(self) -> Scenario:
        if not self.model:
            return self._generate_mock_scenario()

        prompt = """
        Generate a disaster scenario for a rescue team.
        Return a JSON object with the following fields:
        - title: Short title of the event.
        - description: Detailed description of the situation.
        - severity: Integer from 1 (minor) to 5 (catastrophic).
        - location: A fictional location name.
        - required_skills: A list of 2-3 skills required to solve this (e.g., "Firefighting", "Medical", "Engineering", "Negotiation").
        """

        try:
            response = await self.model.generate_content_async(prompt)
            # Simple parsing for now - in production use constrained decoding or function calling
            text = response.text.replace("```json", "").replace("```", "")
            data = json.loads(text)
            
            return Scenario(
                id=str(uuid.uuid4()),
                title=data["title"],
                description=data["description"],
                severity=data["severity"],
                location=data["location"],
                required_skills=data["required_skills"]
            )
        except Exception as e:
            print(f"Error generating scenario: {e}")
            return self._generate_mock_scenario()

    def _generate_mock_scenario(self) -> Scenario:
        return Scenario(
            id=str(uuid.uuid4()),
            title="Mock Chemical Spill",
            description="A chemical truck has overturned on the highway, leaking hazardous material.",
            severity=3,
            location="Sector 7 Highway",
            required_skills=["Hazmat", "Medical"]
        )
