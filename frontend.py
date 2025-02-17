import streamlit as st
from api_handler import generate_response
from conversation_logger import configure_papertrail_logging

# Configure papertrail-logging
logger = configure_papertrail_logging()

# Streamlit app
st.title("PA Navigator")

# Maintain conversation history
if "history" not in st.session_state:
    st.session_state["history"] = [
        {"role": "system", "content": (
            ""
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
            
            logger.info(f"User Prompt: {user_input}")
            logger.info(f"Assistant Response: {gpt_response}")

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