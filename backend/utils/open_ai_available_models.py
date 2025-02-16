import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key not found. Make sure OPENAI_API_KEY is set in .env")

# Set the OpenAI API key
openai.api_key = api_key

# Fetch and print available models
models = openai.models.list()
for model in models['data']:
    print(model['id'])