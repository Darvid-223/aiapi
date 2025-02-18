import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("OPENAI_API_KEY")
ASSISTANT_ID = os.environ.get("ASSISTANT_ID")


client = OpenAI(api_key=API_KEY)


assistant = client.beta.assistants.update(
    assistant_id=ASSISTANT_ID,
)

# Global variabel för att spara en thread (om du vill behålla kontext över flera rundor)
_thread = None

def get_thread():
    global _thread
    if _thread is None:
        _thread = client.beta.threads.create()
        print(f"Created new thread with id: {_thread.id}")
    return _thread

def generate_response(history: list) -> str:
    """
    Generates a response from the assistant (with file search enabled)
    using beta-threads. The conversation history (a list of messages) is added
    to a thread, and then the assistant is run on that thread.
    """
    thread = get_thread()
    
    # Lägg till alla meddelanden (endast 'user' och 'assistant') i threaden.
    for msg in history:
        if msg["role"] not in ["user", "assistant"]:
            continue
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role=msg["role"],
            content=msg["content"],
        )
    
    # Kör assistenten på threaden och vänta på svar.
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
    
    # Hämta meddelandena från den körda run:en.
    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    # Här antar vi att svaret finns i den första meddelande-posten, 
    # och att innehållet finns i messages[0].content[0].text.value.
    # Anpassa beroende på API:s svarstruktur.
    message_content = messages[0].content[0].text
    return message_content.value
