
from typing import List
from app.models import Scenario, Survivor, Mission
import uuid
import math
import numpy as np

# Reference Incident Coordinate (San Francisco Center)
INCIDENT_LAT = 37.7749
INCIDENT_LON = -122.4194

# Simulated locations for default mock database survivors (lat, lon)
SURVIVOR_LOCATIONS = {
    "Alex": (37.7891, -122.4014),
    "Sam": (37.7564, -122.4431),
    "Jordan": (37.7011, -122.4611),
    "Casey": (38.0124, -122.1245),
    "Morgan": (37.7749, -122.4194),  # on-scene
    "Riley": (37.6879, -122.4014),
    "Quinn": (37.8044, -122.2711)
}

def haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return c * 6371

class Coordinator:
    def __init__(self):
        self.model = None  # Force local analytical engine

    async def assign_team(self, scenario: Scenario, survivors: List[Survivor]) -> Mission:
        scored_survivors = []
        required_skill = scenario.required_skills[0] if scenario.required_skills else "Rescue"

        for s in survivors:
            if s.status != "On-Call":
                continue

            # Resolve coordinates or default
            lat, lon = SURVIVOR_LOCATIONS.get(s.name, (37.7749, -122.4194))
            dist = haversine_distance(lat, lon, INCIDENT_LAT, INCIDENT_LON)

            # Skill level
            skill_level = s.skills.get(required_skill, 0)

            # 1. Travel Fatigue & Skill Protection factors
            fatigue_factor = min(0.3, dist / 100.0)
            skill_protection = min(0.2, skill_level * 0.05)

            # 2. Probability Transitions
            p_healthy_to_exhausted = max(0.05, 0.2 + fatigue_factor - skill_protection)
            p_exhausted_to_injured = max(0.02, 0.15 + fatigue_factor - skill_protection)

            # 3. Estimating Survivability P_surv analytically
            p_surv = (1.0 - (p_healthy_to_exhausted * p_exhausted_to_injured)) ** 6

            # 4. Core Selection Utility score: U(d, S_k)
            overall_score = 0.7 * p_surv + 0.3 * (1.0 / (dist + 1.0))

            scored_survivors.append({
                "id": s.id,
                "name": s.name,
                "score": overall_score,
                "dist": dist
            })

        # Sort by best score
        scored_survivors.sort(key=lambda x: x["score"], reverse=True)
        selected_ids = [s["id"] for s in scored_survivors[:3]]
        selected_names = [s["name"] for s in scored_survivors[:3]]

        print(f"Selected deployment team: {selected_names}")

        return Mission(
            id=str(uuid.uuid4()),
            scenario_id=scenario.id,
            assigned_team=selected_ids,
            log=[f"System Coordinator selected team based on analytical utility score: {', '.join(selected_names)}"]
        )
