import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# MODEL_NAME = "deepseek/deepseek-chat"

MODEL_NAME = "nvidia/nemotron-3.5-lightning:free"

TEMPERATURE = 0.2

MAX_TOKENS = 800