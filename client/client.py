import httpx
import asyncio

async def call_agent(url,query):
    payload ={
        "jsonrpc":"2.0",
        "method":"execute",
        "params":{"query":query},
        "id":1
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url,json=payload)
        return response.json()["result"]
    
async def main():
        adk_result = await call_agent(
            "http://localhost:8001/rpc",
            "Explain Agentic AI simply"
        )

        final_result = await call_agent(
            "http://localhost:8002/rpc",
            adk_result
        )

        print("\nFINAL RESULT:\n")
        print(final_result)

if __name__ == "__main__":
    asyncio.run(main())
    