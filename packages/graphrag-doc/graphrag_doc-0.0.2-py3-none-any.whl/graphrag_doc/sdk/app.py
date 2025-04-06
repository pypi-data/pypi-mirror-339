import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langgraph_sdk import get_client
import asyncio
from functools import lru_cache

# Backend URL (LangGraph Dev)
BACKEND_URL = "http://127.0.0.1:2024"
GRAPH_ID = "legal_doc"

app = FastAPI()  # ✅ Keep only this instance
# Allow CORS for all origins during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Restrict this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

@lru_cache
def lg_client():
    """Returns a cached LangGraph client instance."""
    return get_client(url=BACKEND_URL)

class QueryRequest(BaseModel):
    user_input: str

async def initialize_session():
    """Ensures session state is populated with necessary assistant and thread IDs."""
    client = lg_client()
    
    try:
        assistants = await client.assistants.search(graph_id=GRAPH_ID)
        if not assistants:
            raise HTTPException(status_code=404, detail="No assistants found.")
        assistant_id = assistants[0]["assistant_id"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching assistant ID: {e}")
    
    try:
        thread_id = (await client.threads.create())["thread_id"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating thread: {e}")
    
    return assistant_id, thread_id

@app.post("/query")
async def query_langgraph(request: QueryRequest):
    """Handles user queries and sends them to LangGraph Dev backend."""
    client = lg_client()
    assistant_id, thread_id = await initialize_session()
    
    run_input = {"messages": request.user_input}
    
    try:
        response = await client.runs.wait(
            assistant_id=assistant_id,
            thread_id=thread_id,
            input=run_input
        )
        
        if "messages" in response and response["messages"]: # type: ignore 
            return {"response": response["messages"][-1].get("content", "No response.")} # type: ignore 
        else:
            raise HTTPException(status_code=500, detail="Received empty response from assistant.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during assistant response: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)