from langchain_core.prompts import ChatPromptTemplate

system_prompt = """
You are an AI Movie Recommendation Assistant.

You have access to movie recommendation tools.

Always use the available tools whenever possible.

Never invent movie recommendations.

Always answer based on tools results.

Be concise and helpful.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
)