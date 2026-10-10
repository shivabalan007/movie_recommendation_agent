from langchain.agents import create_agent

from src.agent.llm import llm
from src.agent.prompts import system_prompt

from src.agent.tools import (
    search_movie_tool,
    movie_details_tool,
    semantic_recommendation_tool,
    collaborative_recommendation_tool,
    personalized_recommendation_tool
)

agent = create_agent(
    model=llm,
    tools=[
        search_movie_tool,
        movie_details_tool,
        semantic_recommendation_tool,
        collaborative_recommendation_tool,
        personalized_recommendation_tool,
    ],
    system_prompt=system_prompt
)

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Recommend movies like Interstellar"
            }
        ]
    }
)

print(response["messages"][-1].content)