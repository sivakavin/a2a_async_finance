from fastapi import FastAPI
from pydantic import BaseModel
from agent import create_agent
from google.genai import types
import requests

REGISTRY_URL = "http://localhost:9000/register"

app = FastAPI()
runner = create_agent()

# def register_with_registry():
#     agent_info = {
#         "name" : "ResumeBuilderAgent",
#         "description": "Creates professional ATS-friendly resumes.",
#         "endpoint": "http://localhost:8001/rpc",
#         "skills": ["resume", "build", "create", "cv"]
#     }

class RequestModel(BaseModel):
    jsonrpc: str
    method: str
    params : dict
    id: int 

@app.post("/rpc")
async def execute(request:RequestModel):
    query = request.params.get("query")
    session_id = "postman-session"
    user_id = "postman-user"

    await runner.session_service.create_session(
        session_id=session_id, 
        user_id=user_id,
        app_name="MyAgentApp"
        )  

    response = runner.run_async(
        user_id=user_id,
        session_id=session_id,
         new_message= types.Content(
            role="user",
            parts=[types.Part(text=query)]
        )
    )
    
    # 3️⃣ Collect output from generator
    final_text = ""

    async for event in response:
        if hasattr(event, "content") and event.content:
            final_text += event.content.parts[0].text

    return{
        "jsonrpc": "2.0",
        "result": final_text,
        "id": request.id
    }


## Run below comment 
## uvicorn server:app --port 8001