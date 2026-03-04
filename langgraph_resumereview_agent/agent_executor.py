from graph import create_graph
from google.genai import types
## Agemt Executor lib
from a2a.server.events import EventQueue
from a2a.types import (
    TextPart
)
from a2a.utils import new_agent_text_message
from a2a.server.agent_execution import AgentExecutor,RequestContext
import uuid

class ResumeReviewerAgentExecutor(AgentExecutor):
    def __init__(self):
        self.graph = create_graph()

    async def execute(self, context, event_queue):
        query = context.get_user_input()

        try:
            state = {
                "input":query,
                "output":""
            }

            result = await self.graph.ainvoke(state)

            final_output = result.get("output"," ")

            if final_output:
                await event_queue.enqueue_event(
                    new_agent_text_message(final_output)
                )
        except Exception as e:
            await event_queue.enqueue_event(
                new_agent_text_message(f"❌ Error: {str(e)}")
            )
    
    async def cancel(self, context, event_queue):
        return await super().cancel(context, event_queue)

