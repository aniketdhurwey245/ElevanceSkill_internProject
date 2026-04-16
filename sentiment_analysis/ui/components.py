import streamlit as st


def render_message(role: str, text: str, sentiment: str = None):
    if role == "user":
        st.markdown(f"""
        <div style='text-align:right;
                    background:#7c3aed;
                    color:white;
                    padding:10px;
                    border-radius:12px;
                    margin:6px'>
            {text}
        </div>
        """, unsafe_allow_html=True)

    else:
        color_map = {
            "positive": "#10b981",
            "negative": "#ef4444",
            "neutral": "#3b82f6"
        }

        border = color_map.get(sentiment, "#3b82f6")

        st.markdown(f"""
        <div style='text-align:left;
                    background:#111827;
                    color:white;
                    padding:12px;
                    border-left:4px solid {border};
                    border-radius:12px;
                    margin:6px'>
            {text}
        </div>
        """, unsafe_allow_html=True)


def sentiment_badge(sentiment: str, intensity: str):
    color_map = {
        "positive": "#10b981",
        "negative": "#ef4444",
        "neutral": "#3b82f6"
    }

    color = color_map.get(sentiment, "#3b82f6")

    st.markdown(f"""
    <span style="
        background:{color}20;
        border:1px solid {color};
        padding:4px 10px;
        border-radius:20px;
        font-size:12px;
        color:{color};
        margin-left:8px">
        {sentiment.upper()} · {intensity}
    </span>
    """, unsafe_allow_html=True)