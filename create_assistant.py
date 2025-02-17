import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get("OPENAI_API_KEY")
ASSISTANT_ID = os.environ.get("ASSISTANT_ID")

client = OpenAI(api_key=API_KEY)

# Create vector store
vector_store = client.beta.vector_stores.create(name="brukare")
print(f"Vector Store Id - {vector_store.id}")

# Upload brukare database
file_paths = ["files/json-brukare-db.json"]
file_streams = [open(path, "rb") for path in file_paths]

# Add files to vector store
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id = vector_store.id,
    files = file_streams
)

# Check the status of files
print(f"File Status {file_batch.status}")

# Update the assistant with vector store
assistant = client.beta.assistants.update(
    assistant_id=ASSISTANT_ID,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)
print("Assistant updated with vector store.")

thread = client.beta.threads.create()
print(f"Your thread Id: {thread.id}\n\n")

while True:
    text = input("What's your question?\n")

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text,
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )

    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    message_content = messages[0].content[0].text
    print("Response: \n")
    print(f"{message_content.value}\n")