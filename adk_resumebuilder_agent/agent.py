from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from dotenv import load_dotenv

load_dotenv()

def create_resume_builder_agent():
    session = InMemorySessionService()

    agent = Agent(
        name="ResumeBuilderAgent",
        description="Creates professional ATS-friendly resumes from raw user details.",
        instruction="""
        You are a professional resume builder.

        Your job:
        - Collect user details (skills, experience, education, projects).
        - Format resume professionally.
        - Use bullet points.
        - Make it ATS-friendly.
        - Keep language strong and achievement-based.
        - If information is missing, ask follow-up questions.

        Output format:
        - Name
        - Summary
        - Skills
        - Experience
        - Projects
        - Education
        """,
        model="gemini-2.5-flash",
    )

    runner = Runner(
        agent=agent,
        session_service=session,
        app_name="ResumeBuilderApp"
    )

    return runner