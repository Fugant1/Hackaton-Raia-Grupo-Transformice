from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, Request
import os

#from agent_workflow.graph.graph import graph, ChatState

@asynccontextmanager
async def lifespan(app: FastAPI):
    # google_api_key = os.getenv("GOOGLE_API_KEY") 
    # app.state.graph = graph(google_api_key, )
    yield

app = FastAPI(title="Unfaker API", version="1.0.0", lifespan=lifespan)

@app.get("/scan", tags=["scanning"])
async def scan(request: Request,url: str = Query(...)):
    return {
        "url": url,
        "score": 0.5,
        "similar_articles": ["https://site1.com", "https://site2.com"],
        "critical_points": [{"trusty": "Test", "tested": "Test"}]
    }
    # graph = request.app.state.graph 

    # result = await graph.ainvoke(ChatState(url=url))
    # tools_info = result.get("tools_info", [])
    # similar_articles = tools_info.get("similar_articles", []) 
    # critical_points = tools_info.get("critical_points", [])

    # return {
    #     "url": url,
    #     "score": result.get("score", 0.0),
    #     "similar_articles": similar_articles,
    #     "critical_points": critical_points
    # }

# uvicorn src.main:app --reload --port 8000