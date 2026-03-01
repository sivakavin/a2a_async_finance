from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from dotenv import load_dotenv

load_dotenv()

def create_agent():
    session = InMemorySessionService()

    # Create an instance of the LlmAgent
    agent = Agent(
        name="MyAgent",
        description="An agent that performs tasks using a language model.",
        instruction="Follow the instructions provided to complete the tasks.",
        model="gemini-2.5-flash-lite",  # Specify the language model to use
    )
    runner = Runner(agent=agent,
                    session_service=session,
                    app_name="MyAgentApp"
                    )
    return runner