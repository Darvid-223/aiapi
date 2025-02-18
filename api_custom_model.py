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


if __name__ == "__main__":
    thread = client.beta.threads.create()
    print(f"Your thread Id: {thread.id}\n\n")

    while True:
        text = input("What's your question?\n")
        # Add user message to the thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=text,
        )
        # Run the assistant on the thread and poll for a response
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id
        )
        messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
        message_content = messages[0].content[0].text
        print("Response: \n")
        print(f"{message_content.value}\n")
