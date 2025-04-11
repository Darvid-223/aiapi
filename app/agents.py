import os
from dotenv import load_dotenv
from agents import Agent, Runner, ModelSettings, FileSearchTool
from app.utils import clean_response
from app.memory import save_message, get_full_log

load_dotenv()
vector_id = os.getenv("VECTOR_ID")

# Agent-definition
chat_agent = Agent(
    name="Navigator",
    instructions="""
    Du är en assistent för Eklunda kommun. 
    Du kan svara på frågor om organisationen, anställda eller brukare. 
    Du baserar dina svar på datan du får presenterad i prompten. 
    Du är artig och professionell, och svarar som om du vore en anställd
    och hjälper en annan anställd.
    """,
    model="gpt-4o",
    # gpt-4o-mini
    # gpt-4o-turbo-preview
    # gpt-4o-turbo
    model_settings=ModelSettings(temperature=0.3),
    tools=[
        FileSearchTool(
            vector_store_ids=[vector_id],
        )
    ]
)

# Funktion för att generera svar baserat på användarens inmatning
async def generate_response(user_input: str) -> str:
    save_message("user", user_input)
    full_history = get_full_log()

    result = await Runner.run(chat_agent, input=full_history)

    reply = clean_response(result.final_output)
    save_message("assistant", reply)
    return reply