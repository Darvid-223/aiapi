import streamlit as st
from api_custom_model import generate_response, reset_thread
from conversation_logger import configure_papertrail_logging

# Konfigurera logging
logger = configure_papertrail_logging()

st.title("PA Navigator")

# Spara konversationen i session state om den inte redan finns
if "history" not in st.session_state:
    st.session_state["history"] = []

# Inputfält för användarens fråga
user_input = st.text_input("Skriv din fråga:", key="user_input")

# Knapp för att skicka frågan
if st.button("Skicka fråga"):
    if user_input:
        # Lägg till användarens meddelande i historiken
        st.session_state["history"].append({"role": "user", "content": user_input})
        try:
            response = generate_response(user_input)
            st.session_state["history"].append({"role": "assistant", "content": response})
            logger.info(f"User Prompt: {user_input}")
            logger.info(f"Assistant Response: {response}")
        except Exception as e:
            error_message = f"Ett fel inträffade: {e}"
            st.session_state["history"].append({"role": "assistant", "content": error_message})
            st.error(error_message)
        # Töm inputfältet
        st.session_state.user_input = ""

# Visa hela konversationen
st.markdown("### Konversation")
for message in st.session_state["history"]:
    if message["role"] == "user":
        st.markdown(f"**Du:** {message['content']}")
    elif message["role"] == "assistant":
        st.markdown(f"**PA Navigator:** {message['content']}")

# Knapp för att rensa konversationen (skapar en ny tråd)
if st.button("Rensa konversation"):
    reset_thread()
    st.session_state["history"] = []
    st.success("Konversationen har rensats!")
