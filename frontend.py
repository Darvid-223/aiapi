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


# Global variabel för att spara en thread
_thread = None

def get_thread():
    """Returnerar den nuvarande tråden, eller skapar en ny om den inte finns."""
    global _thread
    if _thread is None:
        _thread = client.beta.threads.create()
        print(f"Created new thread with id: {_thread.id}")
    return _thread

def reset_thread():
    """Återställer tråden, så att en ny skapas vid nästa anrop."""
    global _thread
    _thread = None
    print("Thread reset.")

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
    
    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    try:
        # Här antar vi att svaret finns i messages[0].content[0].text.value
        message_content = messages[0].content[0].text.value
    except Exception as e:
        raise Exception(f"Could not parse response: {e}")
    
    return message_content.strip()

if __name__ == "__main__":
    # Terminalbaserat exempel
    while True:
        user_input = input("What's your question?\n")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = generate_response(user_input)
        print("\nAssistant:")
        print(response)
        print("\n")
