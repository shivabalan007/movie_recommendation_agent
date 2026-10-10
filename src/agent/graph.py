from langgraph.graph import StateGraph, START, END
from src.database.connection import checkpointer

from src.agent.state import AgentState
from src.agent.nodes import (
    understand_request,
    search_node,
    movie_details_node,
    semantic_recommendation_node,
    collaborative_recommendation_node,
    personalized_recommendation_node,
    genre_recommendation_node,
    unknown_request_node,
    generate_response,
)

# ROUTER
def route_request(state: AgentState) -> str:
    """
    Decide which workflow node should run based on intent identified by the LLM.
    """

    intent = state.get("intent", "")

    if intent == "search":
        return "search"

    if intent == "movie_details":
        return "movie_details"

    if intent == "semantic_recommendation":
        return "semantic_recommendation"

    if intent == "collaborative_recommendation":
        return "collaborative_recommendation"

    if intent == "personalized_recommendation":
        return "personalized_recommendation"

    if intent == "genre_recommendation":
        return "genre_recommendation"

    return "unknown"

# BUILD GRAPH
def build_graph():
    """
    Build the LangGraph workflow.
    """
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node(
        "understand_request",
        understand_request,
    )

    graph.add_node(
        "search",
        search_node,
    )

    graph.add_node(
        "movie_details",
        movie_details_node,
    )

    graph.add_node(
        "semantic_recommendation",
        semantic_recommendation_node,
    )

    graph.add_node(
        "collaborative_recommendation",
        collaborative_recommendation_node,
    )

    graph.add_node(
        "personalized_recommendation",
        personalized_recommendation_node,
    )

    graph.add_node(
        "genre_recommendation",
        genre_recommendation_node,
    )

    graph.add_node(
        "unknown",
        unknown_request_node,
    )

    graph.add_node(
        "generate_response",
        generate_response,
    )

    # START
    graph.add_edge(
        START,
        "understand_request",
    )

    # LLM → ROUTER

    graph.add_conditional_edges(
        "understand_request",
        route_request,
        {
            "search": "search",
            "movie_details": "movie_details",
            "semantic_recommendation": "semantic_recommendation",
            "collaborative_recommendation": "collaborative_recommendation",
            "personalized_recommendation": "personalized_recommendation",
            "genre_recommendation": "genre_recommendation",
            "unknown": "unknown",
        },
    )

    # TOOL / WORKFLOW NODES → FINAL RESPONSE

    graph.add_edge(
        "search",
        "generate_response",
    )

    graph.add_edge(
        "movie_details",
        "generate_response",
    )

    graph.add_edge(
        "semantic_recommendation",
        "generate_response",
    )

    graph.add_edge(
        "collaborative_recommendation",
        "generate_response",
    )

    graph.add_edge(
        "personalized_recommendation",
        "generate_response",
    )

    graph.add_edge(
        "genre_recommendation",
        "generate_response",
    )

    graph.add_edge(
        "unknown",
        "generate_response",
    )

    # FINAL

    graph.add_edge(
        "generate_response",
        END,
    )

    return graph.compile(checkpointer=checkpointer)


# COMPILED GRAPH


movie_agent_graph = build_graph()


# TEST

if __name__ == "__main__":

    print("\n========================================")
    print("Testing LangGraph Memory")
    print("========================================")

    config = {
        "configurable": {
            "thread_id": "test_conversation_2"
        }
    }

    # -----------------------------------------------------
    # TURN 1
    # -----------------------------------------------------

    # result = movie_agent_graph.invoke(
    #     {
    #         "user_input": "Give me details about Interstellar",
    #         "status": "started",
    #     },
    #     config=config
    # )

    # print("\n========================================")
    # print("TURN 1")
    # print("========================================")

    # print(result.get("final_response"))


    # -----------------------------------------------------
    # TURN 2
    # -----------------------------------------------------

    result = movie_agent_graph.invoke(
        {
            "user_input": "What year was it released?",
            "status": "started",
        },
        config=config
    )

    print("\n========================================")
    print("TURN 2")
    print("========================================")

    print(result.get("final_response"))