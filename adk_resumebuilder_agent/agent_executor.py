## Agent Detail
from agent import create_resume_builder_agent
from google.genai import types
## Agemt Executor lib
from a2a.server.events import EventQueue
from a2a.types import (
    TextPart
)
from a2a.utils import new_agent_text_message
from a2a.server.agent_execution import AgentExecutor,RequestContext
import uuid

class ResumeBuilderAgentExecutor(AgentExecutor):
    def __init__(self):
        self.runner = create_resume_builder_agent()

    async def execute(self, context:RequestContext, event_queue:EventQueue):
        query = context.get_user_input()
        try:
            user_content = types.Content(role='user',
                                         parts=[types.Part(text=query)])
            session_id = str(uuid.uuid4())
            user_id = str(uuid.uuid4())

            # Create session before running
            await self.runner.session_service.create_session(
                session_id=session_id,
                user_id=user_id,
                app_name="ResumeBuilderApp"
            )

            async for event in self.runner.run_async(
                user_id = user_id,
                session_id = session_id,
                new_message = user_content
            ):
                if event.content:
                    final_text = event.content.parts[0].text if event.content.parts else ""
                    if final_text:
                        await event_queue.enqueue_event(new_agent_text_message(final_text))


        except Exception as e:
            await event_queue.enqueue_event(
                new_agent_text_message(f"❌ Error: {str(e)}")
            )

    async def cancel(self, context, event_queue):
        return await super().cancel(context, event_queue)