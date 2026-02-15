Project Analysis: Google Cloud AI Rescue Coordinator

1. The Core Concept: "From Search to Simulation"

The original Survivor Network Codelab focuses on Discovery: finding the right person for a static problem using Spanner and Vector Search.
Your proposal adds Time & Evolution:

Dynamic Personnel: Agents that learn and change stats based on experience.

The Coordinator: An AI that manages the trade-off between solving the crisis now (Exploitation) and training for the future (Exploration).

Synthetic Training: Using AI to simulate the crisis itself so the "Coordinator" can practice without real-world stakes.

2. Architecture Extensions

To implement this, we need to add a "Simulation Loop" and an "Evaluation Engine" to the existing Codelab architecture.

The "Loop" Architecture

The World Engine (Cloud Run): Generates random crisis scenarios (e.g., "Chemical spill in Sector 7").

The Coordinator (Gemini 1.5 Pro): Reads the crisis, queries the Spanner Graph for available agents, and assigns a team.

Logic: "I need one expert to fix the leak, but I'll assign Rookie Agent B to observe and learn."

The Mission Sim (Vertex AI Agents): The assigned agents "play out" the scenario in a chat-based environment. They use their tools (from the Codelab) to attempt a solution.

The After-Action Report (Gemini 1.5 Flash): An evaluator model reads the mission logs.

Did they succeed?

Did the rookie learn anything?

State Update (Spanner): The evaluator updates the agents' skill nodes in the Graph Database.

Database Schema Updates (Spanner Graph)

We need to evolve the schema to support "Growth."

-- Existing Node
(Survivor)

-- New Properties for Survivor Nodes
status: "On-Call" | "Deployed" | "Resting"
xp_points: Integer
traits: ["Quick Learner", "Prodigy", "Hesitant"]

-- New Edge: MENTORING
(Survivor: Veteran)-[MENTORS]->(Survivor: Rookie)

-- New Edge: COMPLETED_MISSION
(Survivor)-[COMPLETED]->(Mission)
  properties: { performance_rating: 5, skills_used: ["First Aid", "Leadership"] }


3. Implementation Strategy

Phase 1: The Synthetic Personnel (The "Sims")

Instead of static profiles, each personnel member is a Vertex AI Agent with a specific system_instruction.

The Prompt: "You are 'Rookie Sarah'. You have high potential in Mechanics but low confidence. You hesitate before acting."

Evolution: When Spanner updates her skills, we programmatically update her system prompt. "You are now 'Specialist Sarah'. You are confident in Mechanics."

Phase 2: The "Prodigy" Detector

This is the "fun" part you mentioned. We use Anomaly Detection on the mission results.

Standard Logic: A rookie usually solves a Level 5 fire problem in 10 turns.

The Prodigy Event: If a rookie solves it in 2 turns with a novel solution, the Evaluator flags them as a "Prodigy."

Coordinator Action: The Coordinator AI gets a notification: "New Talent Discovered. Re-routing training priority."

Phase 3: The Coordinator (Reinforcement Learning Lite)

The Coordinator isn't just a chatbot; it's an optimization engine.

Input: Crisis severity, available staff, current skill gaps.

Goal: Maximize (Mission Success Rate + Total Skill Growth).

Decision: "I will send the Expert to the high-risk zone. I will cycle the intermediate team to the low-risk zone to grind XP."

4. Why This Matters (Real World Use Cases)

While "fun," this architecture mirrors advanced enterprise needs:

SRE On-Call Training: Simulating outages to train Junior SREs before they get paged at 3 AM.

Customer Support routing: Sending easy tickets to newbies and hard tickets to veterans, while occasionally giving newbies a "reach" task to test growth.

Dynamic Team Building: Using Graph databases to find the best combination of personalities, not just skills.

5. Proposed Stack

Frontend: The existing Codelab 3D Visualizer (Three.js).

Backend: FastAPI on Cloud Run.

Database: Google Cloud Spanner (Graph).

AI Models:

Coordinator: Gemini 1.5 Pro (Reasoning).

Agents/Sim: Gemini 1.5 Flash (Speed/Cost).

Prodigy Detection: BigQuery ML (Log analysis).
