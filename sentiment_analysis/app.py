import streamlit as st
from core.chatbot_engine import AdvancedChatbot
from core.analytics import log_interaction
from ui.dashboard import render_dashboard

st.set_page_config(layout="wide")

if "bot" not in st.session_state:
    st.session_state.bot = AdvancedChatbot()
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🧠 Advanced Emotion-Aware Chatbot")

tab1, tab2 = st.tabs(["💬 Chat", "📊 Analytics"])

# CHAT TAB
with tab1:
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Type your message...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        result = st.session_state.bot.process(user_input)

        log_interaction(user_input, result["emotion"])

        st.session_state.messages.append({
            "role": "assistant",
            "content": f"{result['response']}\n\n🧠 Emotion: {result['emotion']['emotion']} ({result['emotion']['intensity']})"
        })

        st.rerun()

# ANALYTICS TAB
with tab2:
    render_dashboard()