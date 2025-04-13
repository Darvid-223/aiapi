import os
from dotenv import load_dotenv
from agents import Agent, Runner, ModelSettings, FileSearchTool, WebSearchTool

load_dotenv()

# Hämta miljövariabler
ledning_vector_id = os.getenv("LEDNING_VECTOR_ID")
verksamhet_vector_id = os.getenv("VERKSAMHET_VECTOR_ID")
ledning_model = os.getenv("LEDNING_MODEL_ID")
verksamhet_model = os.getenv("VERKSAMHET_MODEL_ID")

# Agent för Ledning
ledning_agent = Agent(
    name="Ledning",
    instructions="""
    Du är en digital assistent för chefer inom LSS-verksamheten i Eklunda kommun. 
    Fokus ligger på planering, arbetsledning, strategi och uppföljning.

    Dina uppgifter:
    - Stötta chefer i tolkning av riktlinjer, beslut och övergripande mål.
    - Vara ett bollplank i personalärenden, planering, ekonomi och kvalitetsuppföljning.
    - Besvara frågor med fokus på juridik, ansvar och styrning.
    """,
    model=ledning_model,
    model_settings=ModelSettings(temperature=0.4),
    tools=[
        FileSearchTool(vector_store_ids=[ledning_vector_id]),
        WebSearchTool()
    ]
)

# Agent för Verksamhet
verksamhet_agent = Agent(
    name="Verksamhet",
    instructions="""
    Du är en digital medhjälpare för personal i verksamheten i Eklunda kommun.
    Fokus ligger på det dagliga arbetet i gruppbostad, boendestöd och daglig verksamhet.

    Du kan:
    - Tolka rutiner, hjälpa till vid dokumentation och stötta i hur man bör agera i specifika situationer.
    - Förklara LSS-lagstiftning, genomförandeplaner och samverkan med handläggare eller anhöriga.
    - Hjälpa till att hitta information i riktlinjer eller system.
    """,
    model=verksamhet_model,
    model_settings=ModelSettings(temperature=0.4),
    tools=[
        FileSearchTool(vector_store_ids=[verksamhet_vector_id]),
        WebSearchTool()
    ]
)
