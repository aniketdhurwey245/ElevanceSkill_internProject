import streamlit as st
from backend import get_text_response, get_image_response
from image_utils import load_image

# Page setup
st.set_page_config(
    page_title="Multimodal AI Chatbot",
    page_icon="",
    layout="wide"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
/* Main background */
body {
    background-color: #0E1117;
}

/* Header */
.header {
    text-align: center;
    padding: 10px;
    font-size: 28px;
    font-weight: bold;
    color: #FFFFFF;
}

/* Chat container */
.chat-box {
    max-width: 850px;
    margin: auto;
}

/* User message */
.user {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    color: white;
    padding: 12px;
    border-radius: 15px;
    margin: 8px 0;
    text-align: right;
}

/* Bot message */
.bot {
    background: #1E1E1E;
    color: #EAEAEA;
    padding: 12px;
    border-radius: 15px;
    margin: 8px 0;
    text-align: left;
}

/* Footer */
.footer {
    text-align: center;
    color: gray;
    font-size: 12px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown('<div class="header">🤖 Multimodal AI Chatbot</div>', unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.markdown("## ⚙️ Controls")

    uploaded_file = st.file_uploader("📤 Upload Image", type=["png", "jpg", "jpeg"])

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.write("This chatbot uses Gemini AI to process text and images.")

# ------------------ SESSION ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------ CHAT DISPLAY ------------------
st.markdown('<div class="chat-box">', unsafe_allow_html=True)

for role, msg in st.session_state.messages:
    if role == "user":
        st.markdown(f'<div class="user">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot">{msg}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ------------------ INPUT ------------------
user_input = st.chat_input("💬 Ask something or upload an image...")

# ------------------ PROCESS ------------------
if user_input:
    with st.spinner("🤖 Thinking..."):
        if uploaded_file:
            image = load_image(uploaded_file)
            response = get_image_response(image, user_input)
        else:
            response = get_text_response(user_input)

    st.session_state.messages.append(("user", user_input))
    st.session_state.messages.append(("bot", response))

    st.rerun()

# ------------------ FOOTER ------------------
st.markdown('<div class="footer">Built with ❤️ using Streamlit & Gemini AI</div>', unsafe_allow_html=True)