import streamlit as st
import pandas as pd
import json

def render_dashboard():
    try:
        with open("data/logs.json") as f:
            data = json.load(f)
    except:
        st.warning("No data yet")
        return

    df = pd.DataFrame(data)

    st.subheader("📊 Sentiment Analytics")
    st.bar_chart(df["emotion"].value_counts())