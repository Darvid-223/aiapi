import streamlit as st
from api_handler import generate_response

# Streamlit app
st.title("PA Navigator")

# Maintain conversation history
if "history" not in st.session_state:
    st.session_state["history"] = [
        {"role": "system", "content": (
            "You are an assistant for a workplace called 'Eklunda kommun'. Your purpose is to help employees "
            "find information about the organization and its staff. You have access to a PostgreSQL database that contains "
            "detailed information about employees, such as their names, roles, ages, and genders. Use this database when answering "
            "questions about specific people."
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
st.text_input("Du:", key="user_input", placeholder="Write your message here...", on_change=send_message)

# "Clear Conversation" button to reset the history (excluding the system message)
if st.button("Rensa konversation"):
    st.session_state["history"] = [st.session_state["history"][0]]  # Behåll endast systemmeddelandet
