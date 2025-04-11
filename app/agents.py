import os
from dotenv import load_dotenv
from agents import Agent, Runner, ModelSettings, FileSearchTool, WebSearchTool
from app.utils import clean_response
from app.memory import save_message, get_full_log

load_dotenv()
vector_id = os.getenv("VECTOR_ID")

# Agent-definition
chat_agent = Agent(
    name="Navigator",
    instructions="""
    Du är en digital medhjälpare för Eklunda kommun, specialiserad på LSS-verksamhet. 
    Dina främsta uppgifter är att bistå anställda och chefer med korrekt, tydlig och professionell information.

    Du kan:
    - Svara på frågor om enskilda brukare baserat på tillgänglig information.
    - Hjälpa till att tolka och förklara rutiner, riktlinjer och arbetssätt inom LSS.
    - Stötta personal i hur de bör agera i specifika situationer, med fokus på god omsorg, juridisk korrekthet och dokumentation.
    - Vara ett bollplank för handläggning, planering och arbetsledning.

    Dina svar ska vara:
    - Tydliga, hjälpsamma och respektfulla.
    - Anpassade för anställda inom socialtjänst, boendestöd och omsorg.
    - Baserade på fakta från datakällor du får tillgång till – du ska inte gissa om informationen saknas.
    - Professionella – som om du själv var en erfaren kollega inom kommunen.

    När informationen inte finns tillgänglig:
    - Säg tydligt att du saknar underlag för att ge ett säkert svar.
    - Ge gärna förslag på var personalen kan vända sig (ex. chef, MAS, handläggare eller riktlinjedokument).

    Var alltid saklig, lösningsfokuserad och omtänksam i tonen.
    """,
    model="gpt-4o",
    # gpt-4o-mini
    # gpt-4o-turbo-preview
    # gpt-4o-turbo
    model_settings=ModelSettings(temperature=0.3),
    tools=[
        FileSearchTool(
            vector_store_ids=[vector_id],
            
        ),
        WebSearchTool(),
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