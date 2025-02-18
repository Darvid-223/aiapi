import streamlit as st
from api_custom_model import generate_response
from conversation_logger import configure_papertrail_logging

# Configure papertrail-logging
logger = configure_papertrail_logging()

st.title("PA Navigator")
st.text("OBS: Allt som skrivs här loggas.")

# Behåll konversationen i session state.
if "history" not in st.session_state:
    st.session_state["history"] = [
        {"role": "system", "content": (
            "You are an assistant for Eklunda kommun with access to file search tools. "
            "Use the provided documents to answer questions about the organization and its employees."
        )}
    ]

def send_message():
    user_input = st.session_state.user_input.strip()
    if user_input:
        # Lägg till användarens meddelande.
        st.session_state["history"].append({"role": "user", "content": user_input})
        
        try:
            # Hämta svaret från assistenten med hela konversationens historik.
            gpt_response = generate_response(history=st.session_state["history"])
            st.session_state["history"].append({"role": "assistant", "content": gpt_response})
            
            logger.info(f"User Prompt: {user_input}")
            logger.info(f"Assistant Response: {gpt_response}")
        except Exception as e:
            st.session_state["history"].append({"role": "assistant", "content": f"An error occurred: {e}"})
            st.error(f"An error occurred: {e}")
        
        st.session_state.user_input = ""

# Visa konversationen (utom systemmeddelandet)
for message in st.session_state["history"]:
    if message["role"] == "system":
        continue
    role = "Du" if message["role"] == "user" else "PA Navigator"
    st.markdown(f"**{role}:** {message['content']}")

st.text_input("Du:", key="user_input", placeholder="Skriv din fråga här...", on_change=send_message)

if st.button("Rensa konversation"):
    st.session_state["history"] = [st.session_state["history"][0]]
