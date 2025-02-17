import os
from openai import OpenAI
from dotenv import load_dotenv


# Load .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def generate_response(history: list, assistant_id: str) -> str:
    """
    Generates a response from OpenAI based on the provided conversation history.
    Uses the assistant (with file search) that was created via beta-assistants.
    """
    try:
        # Send the entire conversation history to OpenAI API
        response = client.beta.assistants.create(
            assistant_id=assistant_id,
            messages=history
        )
        # Extract and return the response text
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    # Initialize conversation history with a system message if 'API_handler.py' is executed
    conversation_history = [
        {"role": "system", "content": (
            "You are an assistant for a workplace called 'Eklunda kommun'. Your purpose is to help employees "
            "find information about the organization and its staff. You have access to a PostgreSQL database that contains "
            "detailed information about employees, such as their names, roles, ages, and genders. Use this database when answering "
            "questions about specific people."
        )}
    ]

    print("Welcome to the Workplace Assistant!")
    while True:
        user_prompt = input("\nEnter your question (or 'exit' to quit): ")
        if user_prompt.lower() == "exit":
            print("Goodbye!")
            break

        # Add user's input to the conversation history
        conversation_history.append({"role": "user", "content": user_prompt})

        # Generate a response from OpenAI
        response = generate_response(history=conversation_history)

        # Add the assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response})

        # Print the assistant's response
        print(f"\nAssistant: {response}")
