import streamlit as st
from api_handler import generate_response
from connect_to_db import query_database
from conversation_logger import log_conversation

# Streamlit app
st.title("PA Navigator")

# Maintain conversation history
if "history" not in st.session_state:
    st.session_state["history"] = [
        {"role": "system", "content": (
            "Du är en assistent för en organisation som heter 'Eklunda kommun'. Ditt syfte är att hjälpa anställda "
            "att hitta information om organisationen och dess personal. Du har tillgång till en PostgreSQL-databas "
            "som innehåller detaljerad information om anställda, såsom deras namn, roller, ålder och kön. "
            "Använd denna databas när du svarar på frågor om specifika personer. "
        )}
    ]

# Function to handle sending messages
def send_message():
    user_input = st.session_state.user_input.strip()
    if user_input:
        # Add user's message to the history
        st.session_state["history"].append({"role": "user", "content": user_input})

        # Fetch ChatGPT's response with the full conversation history
        try:
            gpt_response = generate_response(history=st.session_state["history"])
            st.session_state["history"].append({"role": "assistant", "content": gpt_response})

            # log promts and answers
            log_conversation(prompt=user_input, response=gpt_response)

        except Exception as e:
            st.session_state["history"].append({"role": "assistant", "content": f"An error occurred: {e}"})
            st.error(f"An error occurred: {e}")

        # Clear the input field
        st.session_state.user_input = ""

# Display the conversation history (excluding the system message)
for message in st.session_state["history"]:
    if message["role"] == "system":
        continue  # Skip displaying the system message
    role = "Du" if message["role"] == "user" else "PA Navigator"
    st.markdown(f"**{role}:** {message['content']}")

# Input field with a key for session state
st.text_input("Du:", key="user_input", placeholder="Skriv din fråga här...", on_change=send_message)

# "Clear Conversation" button to reset the history (excluding the system message)
if st.button("Rensa konversation"):
    st.session_state["history"] = [st.session_state["history"][0]]  # Keep system message only