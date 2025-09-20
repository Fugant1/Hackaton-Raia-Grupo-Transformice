from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
import os

from src.agent_workflow.graph.graph import graph, ChatState

@asynccontextmanager
async def lifespan(app: FastAPI):
    google_api_key = os.getenv("GOOGLE_API_KEY") 
    app.state.graph = graph(google_api_key, None)
    yield

app = FastAPI(title="Unfaker API", version="1.0.0", lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,
    allow_methods=["*"],         
    allow_headers=["*"],        
)

@app.get("/scan", tags=["scanning"])
async def scan(request: Request,post_text: str = Query(...)):
    graph = request.app.state.graph 

    result = await graph.ainvoke(ChatState(post_text=post_text))
    tools_info = result.get("tools_info", [])
    similar_articles = tools_info.get("similar_articles", []) 
    return {
         "post_text": result.get("post_text", ""),
         "score": 0.5,
         "metrics": {"metric1": 0.8, "metric2": 0.6, "metric3": 0.9},
         "similar_articles": similar_articles,
         "critical_points": [{"trusty": "Test", "tested": "Test"}]
    }
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