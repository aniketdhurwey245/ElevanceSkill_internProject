import streamlit as st

from utils.language_detector import detect_language
from utils.translator import translate_text
from utils.response_generator import generate_response
from utils.cultural_adapter import adapt_response
from utils.memory import save_conversation
from components.chat_ui import render_chat

st.set_page_config(page_title="🌍 Multilingual Chatbot", layout="wide")

st.title("🌍 AI Multilingual Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Input
user_input = st.text_input("Ask anything...")

if st.button("Send") and user_input:
    
    # Step 1: Detect language
    lang = detect_language(user_input)

    # Step 2: Translate to English (processing language)
    translated_input = translate_text(user_input, "en")

    # Step 3: Generate response
    raw_response = generate_response(translated_input)

    # Step 4: Translate back to user language
    final_response = translate_text(raw_response, lang)

    # Step 5: Cultural adaptation
    final_response = adapt_response(final_response, lang)

    # Save memory
    save_conversation(user_input, final_response, lang)

    # Store messages
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "bot", "content": final_response})

# Display chat
render_chat(st.session_state.messages)