from fastapi import FastAPI

from src.api.schemas import ChatRequest, ChatResponse
from src.agent.graph import movie_agent_graph

app = FastAPI(
    title="AI Movie Recommendation API",
    description="Backend API for the AI Movie Recommendation Agent",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "movie-recommendation-agent",
    }

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    config = {
        "configurable": {
            "thread_id": request.conversation_id
        }
    }

    result = movie_agent_graph.invoke(
        {
            "user_input": request.message,
            "status": "started",
        },
        config=config,
    )

    return ChatResponse(
        conversation_id=request.conversation_id,
        response=result.get(
            "final_response",
            "Sorry, I couldn't generate a response.",
        ),
    )
