from fastapi import FastAPI
from pydantic import BaseModel
from graph import create_graph

app = FastAPI()
graph = create_graph()

class RequestModel(BaseModel):
    jsonrpc: str
    method: str
    params: dict
    id: int

@app.post("/rpc")
async def execute(request:RequestModel):
    query = request.params.get("query"," ")

    result = await graph.ainvoke({"input": query})

    print("................................")
    print(result)
    print("................................")
    
    return {
        "jsonrpc": "2.0",
        "result": result["output"],
        "id": request.id
    }

## Run below comment 
## uvicorn server:app --port 8002