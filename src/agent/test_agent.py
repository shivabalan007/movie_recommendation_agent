from langchain.agents import create_agent

from src.agent.llm import llm
from src.agent.tools import (
    search_movie_tool,
    movie_details_tool,
    semantic_recommendation_tool,
    collaborative_recommendation_tool,
    personalized_recommendation_tool,
    genre_rerank_tool
)


agent = create_agent(
    model=llm,
    tools=[
        search_movie_tool,
        movie_details_tool,
        semantic_recommendation_tool,
        collaborative_recommendation_tool,
        personalized_recommendation_tool,
        genre_rerank_tool
    ],
    system_prompt="""
You are an AI Movie Assistant.

Use the available tools to answer movie-related questions.

Rules:
- Use search_movie_tool when the user wants to search for movies.
- Use movie_details_tool when the user asks for information about a specific movie.
- Use semantic_recommendation_tool when the user asks for movies similar to another movie.
- Never invent information that should come from a tool.
- Never claim that you used a tool unless you actually used it.
"""
)


def run_test(user_input):

    print("\n================================")
    print("USER:")
    print(user_input)
    print("================================")

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input,
                }
            ]
        }
    )

    print("\nAGENT:")
    print(response["messages"][-1].content, flush=True)


if __name__ == "__main__":

    run_test("Give me genre-based personalized movie recommendations for user shiva")

   

    """run_test("Search for movies containing Inter")

    run_test("Give me details about Interstellar")

    run_test("Recommend movies similar to Interstellar")

     run_test("Recommend movies using collaborative filtering for Interstellar")

     run_test("Give me personalized movie recommendation for user shiva")
    
    """