import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("OPENAI_API_KEY")
ASSISTANT_ID = os.environ.get("ASSISTANT_ID")

client = OpenAI(api_key=API_KEY)

# Uppdatera assistenten med ett existerande vector store-ID (som du redan konfigurerat via dashboard)
vector_store_id_from_dashboard = "vs_67b4eee76d808191ad52c5f88ab42aed"
assistant = client.beta.assistants.update(
    assistant_id=ASSISTANT_ID,
    tool_resources={"file_search": {"vector_store_ids": [vector_store_id_from_dashboard]}},
)
print("Assistant updated with vector store.")

# Global variabel för att spara en thread (om du vill behålla kontext över flera rundor)
_thread = None

def get_thread():
    """Returnerar en existerande thread eller skapar en ny om den inte finns."""
    global _thread
    if _thread is None:
        _thread = client.beta.threads.create()
        print(f"Created new thread with id: {_thread.id}")
    return _thread

def generate_response(user_input: str) -> str:
    """
    Generates a response from the assistant using beta-threads.
    The function adds the user's message to the thread, runs the assistant,
    and returns the assistant's response.
    """
    thread = get_thread()
    
    # Lägg till användarens meddelande i threaden
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input,
    )
    
    # Kör assistenten på threaden och poll:a på ett svar
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
    
    # Hämta meddelandena från run:en
    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    # Beroende på API-strukturen kan svaret finnas på olika ställen.
    # Här antar vi att det första meddelandet i run:en innehåller svaret.
    # Exemplet nedan utgår från att vi kan nå texten via:
    # messages[0].content[0].text.value
    try:
        message_content = messages[0].content[0].text.value
    except Exception as e:
        raise Exception(f"Could not parse response: {e}")
    
    return message_content.strip()

if __name__ == "__main__":
    # Exempelanrop i terminalen
    while True:
        user_input = input("What's your question?\n")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = generate_response(user_input)
        print("\nAssistant:")
        print(response)
        print("\n")
