import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from agent_executor import ResumeReviewerAgentExecutor

def main(host: str = "0.0.0.0", port: int = 8002):
    """
    Bootstraps and starts the Resume Builder Agent server.
    """

    # 1️⃣ Define capabilities (streaming enabled by default)
    capabilities = AgentCapabilities()

    # 2️⃣ Define agent skill metadata
    skill = AgentSkill(
        id="resume_reviewer",
        name="Resume Reviewer",
        description="Analyzes resumes and provides detailed feedback, ATS optimization suggestions, and improvement recommendations.",
        tags=["resume", "review", "ats", "feedback", "improvement"],
        examples=[
            "Review my resume for ATS compatibility",
            "Suggest improvements for this software engineer resume",
            "Analyze resume and provide professional feedback"
        ]
    )

    # 3️⃣ Public URL correction (important)
    card_host = "localhost" if host == "0.0.0.0" else host

    # 4️⃣ Define AgentCard (agent identity)
    agent_card = AgentCard(
        name="Resume Reviewer Agent",
        description="Reviews resumes and provides structured feedback, ATS optimization guidance, and professional improvement suggestions.",
        url=f"http://{card_host}:{port}",
        version="1.0.0",
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
        capabilities=capabilities,
        skills=[skill], 
    )

    # 5️⃣ Connect Executor
    request_handler = DefaultRequestHandler(
        agent_executor=ResumeReviewerAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    # 6️⃣ Create A2A Server Application
    app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler
    )

    # 7️⃣ Start server
    uvicorn.run(app.build(), host=host, port=port)


if __name__ == "__main__":
    main()