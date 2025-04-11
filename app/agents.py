from dotenv import load_dotenv
from agents import Agent, Runner, ModelSettings
from app.utils import read_json_file, clean_response
from app.memory import save_message, get_full_log

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
    model_settings=ModelSettings(temperature=0.3),

)

# Funktion för att generera svar baserat på användarens inmatning
# och information från JSON-filerna samt tidigare historik.
async def generate_response(user_input: str) -> str:
    employees_data = read_json_file("db/employees.json")
    brukare_data = read_json_file("db/brukare.json")

    # Spara användarens fråga i historiken
    save_message("user", user_input)

    # Läs hela historiken (inkl. tidigare frågor och svar)
    full_history = get_full_log()

    # Lägg till systeminstruktion i början
    system_context = f"Information om anställda:\n{employees_data}\n\nInformation om brukare:\n{brukare_data}"
    messages = [{"role": "system", "content": system_context}] + full_history

    result = await Runner.run(chat_agent, input=messages)

    reply = clean_response(result.final_output)
    save_message("assistant", reply)  # Spara svaret
    return reply