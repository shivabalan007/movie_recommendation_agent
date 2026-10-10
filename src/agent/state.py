from typing import Any, TypedDict
from langgraph.graph.message import add_messages
from typing_extensions import Annotated


class AgentState(TypedDict, total=False):
    """
    Shared state for the LangGraph movie recommendation workflow.

    Each LangGraph node reads from this state and can update specific fields.
    """
    user_input: str

    intent: str
    username: str
    movie_name: str
    query: str

    tool_name: str
    tool_result: Any

    recommendations: list[dict[str, Any]]
    """
        [
            {
                "title": "Prometheus",
                "rating": 7.0,
                "year": 2012,
                "semantic_score": 0.526,
                "cf_score": 0.0,
                "recommendation_score": 2,
                "genre_match": 5,
                "genres": ["Adventure", "Science Fiction"]
            }
        ]
    """
    movie_details: dict[str, Any]
    search_results: list[dict[str, Any]]
    final_response: str
    conversation_id: str
    last_recommendations: list[dict[str, Any]]
    selected_movie:str
    messages: Annotated[list[Any], add_messages]

    error: str | None

    status: str


if __name__ == "__main__":
    state: AgentState = {
        "user_input": "Give me genre-based personalized movie recommendations for shiva",
        "intent": "genre_recommendation",
        "username": "shiva",
        "status": "started",
    }

    print("Agent State:")
    print(state)