import re 

from langchain_core.messages import HumanMessage, AIMessage
from src.agent.state import AgentState
from src.agent.llm import llm

from src.agent.tools import (
    search_movie_tool,
    movie_details_tool,
    semantic_recommendation_tool,
    collaborative_recommendation_tool,
    personalized_recommendation_tool,
    genre_rerank_tool,
)

def understand_request(state: AgentState) -> AgentState:
    """
    Use the LLM to understand the user's request.

    The LLM identifies intent,username,movie name,search query
    """

    state["error"] = None
    state["tool_result"] = None
    state["tool_name"] = ""
    state["search_results"] = []
    state["movie_details"] = {}
    state["recommendations"] = []

    state["username"] = ""
    state["movie_name"] = ""
    state["query"] = ""

    user_input = state.get("user_input", "")

    previous_messages = state.get("messages", [])

    conversation_context = "\n".join(f"{message.type}: {message.content}" for message in previous_messages)

    state["messages"] = [HumanMessage(content=user_input)]

    prompt = f"""
You are the request understanding component of an AI Movie Recommendation Assistant.

Use the previous conversation when interpreting the current request.

Previous conversation:
{conversation_context}

Current user request:
{user_input}

Analyze the user's request and return ONLY this format:

intent: <intent>
username: <username or none>
movie_name: <movie name or none>
query: <search query or none>

Allowed intents:

search
movie_details
semantic_recommendation
collaborative_recommendation
personalized_recommendation
genre_recommendation
unknown

Examples:

User:
Search for movies containing Inter

intent: search
username: none
movie_name: none
query: Inter

User:
Give me details about Interstellar

intent: movie_details
username: none
movie_name: Interstellar
query: none

User:
Recommend movies similar to Interstellar

intent: semantic_recommendation
username: none
movie_name: Interstellar
query: none

User:
Recommend movies using collaborative filtering for Interstellar

intent: collaborative_recommendation
username: none
movie_name: Interstellar
query: none

User:
Give me personalized movie recommendations for user shiva

intent: personalized_recommendation
username: shiva
movie_name: none
query: none

User:
Give me genre-based personalized movie recommendations for user shiva

intent: genre_recommendation
username: shiva
movie_name: none
query: none

User request:
{user_input}
"""

    response = llm.invoke(prompt)

    content = response.content.strip()

    print("\n========== LLM UNDERSTANDING ==========")
    print(content)

    state["status"] = "routing"

    # -----------------------------------------------------
    # Parse the simple structured response from the LLM.
    # -----------------------------------------------------

    for line in content.splitlines():

        line = line.strip()

        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        key = key.strip().lower()
        value = value.strip()

        if value.lower() == "none":
            value = ""

        if key == "intent":
            state["intent"] = value

        elif key == "username":
            state["username"] = value

        elif key == "movie_name":
            state["movie_name"] = value

        elif key == "query":
            state["query"] = value

    
    # Normalize intent and recover missing fields.
    user_text = user_input.strip()
    lower_text = user_text.casefold()

    valid_intents = {
        "search",
        "movie_details",
        "semantic_recommendation",
        "collaborative_recommendation",
        "personalized_recommendation",
        "genre_recommendation",
        "unknown",
    }

    intent = state.get("intent", "").strip().lower()

    if intent not in valid_intents:
        intent = "unknown"

    state["intent"] = intent

    movie_name = state.get("movie_name", "").strip()
    query = state.get("query", "").strip()

    # Recover missing search query.
    if intent == "search" and not query:
        if movie_name:
            state["query"] = movie_name
        else:
            cleaned = re.sub(
                r"^(please\s+)?(search\s+for|find|search|look\s+for)\s+"
                r"(movies?\s+)?(containing\s+|matching\s+)?",
                "",
                user_text,
                flags=re.IGNORECASE,
            ).strip(" .?!")

            if cleaned:
                state["query"] = cleaned

    # Correct movie-details requests classified as searches.
    if (
        intent == "search"
        and re.search(
            r"\b(tell me about|details about|information about|"
            r"movie details|describe)\b",
            lower_text,
        )
    ):
        state["intent"] = "movie_details"

    # Debug output.
    print("\n========== NORMALIZED REQUEST ==========")
    print(f"intent: {state.get('intent', '')}")
    print(f"username: {state.get('username', '')}")
    print(f"movie_name: {state.get('movie_name', '')}")
    print(f"query: {state.get('query', '')}")

    return state


# =========================================================
# SEARCH
# =========================================================

def search_node(state: AgentState) -> AgentState:

    state["status"] = "processing"
    state["tool_name"] = "search_movie_tool"

    query = state.get("query", "")

    if not query:
        state["error"] = "No search query was identified."
        return state

    result = search_movie_tool.invoke(
        {
            "query": query
        }
    )

    state["tool_result"] = result
    state["search_results"] = result

    return state


# =========================================================
# MOVIE DETAILS
# =========================================================

def movie_details_node(state: AgentState) -> AgentState:

    state["status"] = "processing"
    state["tool_name"] = "movie_details_tool"

    movie_name = state.get("movie_name", "")

    if not movie_name:
        state["error"] = "No movie name was identified."
        return state

    result = movie_details_tool.invoke(
        {
            "movie_name": movie_name
        }
    )

    state["tool_result"] = result
    state["movie_details"] = result

    return state


# =========================================================
# SEMANTIC RECOMMENDATION
# =========================================================

def semantic_recommendation_node(state: AgentState) -> AgentState:

    state["status"] = "processing"
    state["tool_name"] = "semantic_recommendation_tool"

    movie_name = state.get("movie_name", "")

    if not movie_name:
        state["error"] = "No movie name was identified."
        return state

    result = semantic_recommendation_tool.invoke(
        {
            "movie_name": movie_name
        }
    )

    state["tool_result"] = result
    state["recommendations"] = result

    return state


# =========================================================
# COLLABORATIVE RECOMMENDATION
# =========================================================

def collaborative_recommendation_node(state: AgentState) -> AgentState:

    state["status"] = "processing"
    state["tool_name"] = "collaborative_recommendation_tool"

    movie_name = state.get("movie_name", "")

    if not movie_name:
        state["error"] = "No movie name was identified."
        return state

    result = collaborative_recommendation_tool.invoke(
        {
            "movie_name": movie_name
        }
    )

    state["tool_result"] = result
    state["recommendations"] = result

    return state


# =========================================================
# PERSONALIZED RECOMMENDATION
# =========================================================

def personalized_recommendation_node(state: AgentState) -> AgentState:

    state["status"] = "processing"
    state["tool_name"] = "personalized_recommendation_tool"

    username = state.get("username", "")

    if not username:
        state["error"] = "No username was identified."
        return state

    result = personalized_recommendation_tool.invoke(
        {
            "username": username
        }
    )

    state["tool_result"] = result
    state["recommendations"] = result

    return state


# =========================================================
# GENRE-BASED PERSONALIZED RECOMMENDATION
# =========================================================

def genre_recommendation_node(state: AgentState) -> AgentState:

    state["status"] = "processing"
    state["tool_name"] = "genre_rerank_tool"

    username = state.get("username", "")

    if not username:
        state["error"] = "No username was identified."
        return state

    result = genre_rerank_tool.invoke(
        {
            "username": username
        }
    )

    state["tool_result"] = result
    state["recommendations"] = result

    return state


# =========================================================
# UNKNOWN REQUEST
# =========================================================

def unknown_request_node(state: AgentState) -> AgentState:

    state["status"] = "processing"

    state["final_response"] = (
        "I can help you search for movies, get movie details, "
        "find similar movies, use collaborative filtering, "
        "or get personalized movie recommendations."
    )

    return state


# =========================================================
# LLM: GENERATE FINAL RESPONSE
# =========================================================

def generate_response(state: AgentState) -> AgentState:
    """
    Use the LLM to convert the tool result into the final
    user-facing response.

    The LLM does not perform the recommendation calculation.
    It only explains the result returned by the tools.
    """

    if state.get("error"):

        state["final_response"] = (
            f"Sorry, I could not complete the request. "
            f"{state['error']}"
        )

        state["status"] = "error"

        return state

    user_input = state.get("user_input", "")
    intent = state.get("intent", "")
    tool_result = state.get("tool_result")

    prompt = f"""
You are the final response component of an AI Movie Recommendation Assistant.

Answer the user's request using ONLY the information contained
in the tool result.

Do not invent movies, ratings, genres, scores, or other information.

Be concise and helpful.

User request:
{user_input}

Request intent:
{intent}

Tool result:
{tool_result}

Generate the final answer for the user.
"""

    response = llm.invoke(prompt)

    state["final_response"] = response.content.strip()
    state["messages"] = [AIMessage(content=response.content.strip())]
    state["status"] = "completed"
    return state