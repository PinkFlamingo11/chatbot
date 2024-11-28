import os
import streamlit as st
import openai
from dotenv import load_dotenv

load_dotenv()

# OpenAI API-Schlüssel hier einfügen
openai.api_key = os.getenv("OPEN_AI_KEY")  

# Titel und Beschreibung der App
st.title("Ask GPT-3.5 Turbo")
st.write("""
This app allows you to interact with OpenAI's GPT-3.5 Turbo. 
Type a question below, and click 'Send' to receive a response.
""")

# Eingabefeld für Benutzer
user_input = st.text_area("Enter your question here:", height=100, placeholder="What would you like to know?")

# Antwort in der Session initialisieren
if "response" not in st.session_state:
    st.session_state.response = ""

# Buttons für "Send" und "Refresh"
col1, col2 = st.columns(2)

with col1:
    if st.button("Send"):
        if not user_input.strip():
            st.warning("Please enter a question!")
        else:
            try:
                with st.spinner("Fetching response from GPT-3.5 Turbo..."):
                    # API-Aufruf an OpenAI
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": user_input}
                        ]
                    )
                    # Antwort speichern
                    st.session_state.response = response['choices'][0]['message']['content']
            except Exception as e:
                st.error(f"An error occurred: {e}")

with col2:
    if st.button("Refresh"):
        st.session_state.response = ""
        user_input = ""

# Antwort anzeigen
st.text_area("Response:", value=st.session_state.response, height=150, disabled=True)
