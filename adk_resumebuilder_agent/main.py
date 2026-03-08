import sys
import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import (
    InMemoryTaskStore    
)
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill
)
from fastapi import FastAPI

from agent_executor import ResumeBuilderAgentExecutor

def main(host='0.0.0.0',port=8001):
    """ Start Resume builder agent"""
    ## Functionality used to define pushnotification /streaming
    capabilities = AgentCapabilities(
    streaming=True
)

    ## Used to define agent information
    skill = AgentSkill(
        id = "resume_Builder",
        name = "Resume Builder",
        description="Creates professional ATS-friendly resumes from raw user details.",
        tags = ["resume", "build", "create", "cv"],
        examples=["build resume for agentic developer with all required information"]
                    )
    # Use localhost in the URL if binding to 0.0.0.0 (since 0.0.0.0 is not valid for client connections)
    card_host = 'localhost' if host == '0.0.0.0' else host

    ## defining agent card
    agend_card = AgentCard(
        name = "Resume Builder Agent",
        description= "Creates professional ATS-friendly resumes from raw user details.",
        url=f"http://{card_host}:{port}",
        version='1.0.0',
        default_input_modes=['text/plain','application/json'],
        default_output_modes=['text/plain','application/json'],
        capabilities=capabilities,
        skills=[skill,],
    )

    request_handler = DefaultRequestHandler(
        agent_executor= ResumeBuilderAgentExecutor(),
        task_store= InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agend_card,http_handler=request_handler
    )

    ## Enhancing chat feature
    app = FastAPI()
    a2a_app = server.build()
    app.mount("/",a2a_app)

    uvicorn.run(app,host=host,port=port)

if __name__ == "__main__":
    main()