import os
from openai import OpenAI
from dotenv import load_dotenv


# Load .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

ASSISTANT_ID = os.environ.get("ASSISTANT_ID")

