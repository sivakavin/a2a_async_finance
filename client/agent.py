from google.adk.agents import LlmAgent
from google.adk.agents.remote_a2a_agent import (
    AGENT_CARD_WELL_KNOWN_PATH,
    RemoteA2aAgent,
)
from dotenv import load_dotenv
load_dotenv()

# Connect to remote resume agent
resume_builder_agent = RemoteA2aAgent(
    name="resume_builder",
    description="Creates professional ATS-friendly resumes",
    agent_card=f"http://localhost:8001/{AGENT_CARD_WELL_KNOWN_PATH}",
)

resume_review_agent = RemoteA2aAgent(
    name="resume_reviwer",
    description="review resume like professional ATS-friendly resumes",
    agent_card=f"http://localhost:8002/{AGENT_CARD_WELL_KNOWN_PATH}",
)

# Root client agent
root_agent = LlmAgent(
    name="ai_assistant",
    model="gemini-2.5-flash-lite",
    description="Main assistant agent",
    instruction="""
You are a helpful assistant.
If the user asks about resume creation,
delegate the task to the resume_builder sub-agent.
Do not answer resume requests directly.
""",
    sub_agents=[resume_builder_agent,resume_review_agent],
)