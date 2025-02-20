import streamlit as st
from api_custom_model import generate_response
from conversation_logger import configure_papertrail_logging

# Konfigurera logging
logger = configure_papertrail_logging()

st.title("PA Navigator")

# Visa en notis om att all input loggas
st.info("Observera: Allt du skriver här loggas för att kunna förbättra tjänsten.")


# Inputfält för användarens fråga
user_input = st.text_input("Skriv din fråga:", key="user_input")

# Knapp för att skicka frågan
if st.button("Skicka fråga"):
    if user_input:
        try:
            response = generate_response(user_input)
            st.write("**Du:**", user_input)
            st.write("**PA Navigator:**", response)
            logger.info(f"User Prompt: {user_input}")
            logger.info(f"Assistant Response: {response}")
        except Exception as e:
            st.error(f"Ett fel inträffade: {e}")
