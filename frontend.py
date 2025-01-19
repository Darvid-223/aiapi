import streamlit as st
from api_handler import generate_response

# Streamlit app
st.title("PA Navigator")

# Maintain conversation history
if "history" not in st.session_state:
    st.session_state["history"] = []

# Function to handle sending messages
def send_message():
    user_input = st.session_state.user_input.strip()
    if user_input:
        # Add user's message to the history
        st.session_state.history.append({"role": "user", "content": user_input})

        # Fetch ChatGPT's response
        try:
            gpt_response = generate_response(prompt=user_input)
            st.session_state.history.append({"role": "assistant", "content": gpt_response})
        except Exception as e:
            st.session_state.history.append({"role": "assistant", "content": f"An error occurred: {e}"})
            st.error(f"An error occurred: {e}")

        # Clear the input field
        st.session_state.user_input = ""

# Display the conversation history
for message in st.session_state["history"]:
    role = "Du" if message["role"] == "user" else "PA Navigator"
    st.markdown(f"**{role}:** {message['content']}")

# Input field with a key for session state
st.text_input("Du:", key="user_input", placeholder="Write your message here...", on_change=send_message)

# "Clear Conversation" button to reset the history
if st.button("Rensa konversation"):
    st.session_state["history"] = []
