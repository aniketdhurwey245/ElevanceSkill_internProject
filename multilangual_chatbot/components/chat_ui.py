import streamlit as st

def render_chat(messages):
    for msg in messages:
        if msg["role"] == "user":
            st.markdown(f"**🧑 You:** {msg['content']}")
        else:
            st.markdown(f"**🤖 Bot:** {msg['content']}")