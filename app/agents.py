from dotenv import load_dotenv
from agents import Agent, Runner
from app.utils import read_json_file, clean_response

load_dotenv()

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
)

# Funktion för att generera svar baserat på användarens inmatning
# och information från JSON-filerna.
# Denna funktion läser in data från två JSON-filer och skickar dem till agenten
# tillsammans med användarens fråga.
async def generate_response(user_input: str) -> str:
    employees_data = read_json_file("db/employees.json")
    brukare_data = read_json_file("db/brukare.json")

    system_context = f"Information om anställda:\n{employees_data}\n\nInformation om brukare:\n{brukare_data}"

    messages = [
        {"role": "system", "content": system_context},
        {"role": "user", "content": user_input}
    ]

    result = await Runner.run(chat_agent, input=messages)
    return clean_response(result.final_output)
