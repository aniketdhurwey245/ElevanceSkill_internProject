import streamlit as st
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict

# ==============================
# CONFIG
# ==============================

st.set_page_config(
    page_title="ArXiv AI Research Assistant",
    page_icon="🔬",
    layout="wide"
)

ARXIV_API = "http://export.arxiv.org/api/query"
OLLAMA_API = "http://localhost:11434/api/generate"

# ==============================
# SESSION STATE
# ==============================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "papers" not in st.session_state:
    st.session_state.papers = []

# ==============================
# ARXIV FETCH
# ==============================

def fetch_arxiv(query: str, max_results: int = 5) -> List[Dict]:
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
    }

    try:
        res = requests.get(ARXIV_API, params=params, timeout=10)
        return parse_arxiv(res.text)
    except:
        return []

def parse_arxiv(xml_text: str) -> List[Dict]:
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml_text)

    papers = []

    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text
        summary = entry.find("atom:summary", ns).text

        papers.append({
            "title": title.strip(),
            "abstract": summary.strip()
        })

    return papers

# ==============================
# LLM CALL
# ==============================

def call_ollama(prompt: str) -> str:
    try:
        res = requests.post(
            OLLAMA_API,
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=60
        )
        return res.json().get("response", "")
    except:
        return "⚠️ LLM not available. Please start Ollama."

# ==============================
# CONTEXT BUILDER
# ==============================

def build_context(papers: List[Dict]) -> str:
    context = ""
    for i, p in enumerate(papers[:3]):
        context += f"[{i+1}] {p['title']}\n{p['abstract'][:300]}\n\n"
    return context

# ==============================
# ANSWER GENERATION
# ==============================

def generate_answer(query: str, papers: List[Dict]) -> str:
    context = build_context(papers)

    prompt = f"""
You are an expert AI researcher.

Use the following research papers to answer:

{context}

Question: {query}

Answer clearly and in structured format.
"""

    return call_ollama(prompt)

# ==============================
# UI
# ==============================

st.title("🔬 ArXiv Research Chatbot")

# Display chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# ==============================
# INPUT
# ==============================

user_input = st.chat_input("Ask about AI research...")

if user_input:
    # Prevent duplicate execution
    if (
        len(st.session_state.messages) == 0 or
        st.session_state.messages[-1]["content"] != user_input
    ):
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.spinner("Searching papers..."):
            papers = fetch_arxiv(user_input)
            st.session_state.papers = papers

        with st.spinner("Generating answer..."):
            answer = generate_answer(user_input, papers)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "time": datetime.now().strftime("%H:%M")
        })

        st.rerun()

# ==============================
# SHOW PAPERS
# ==============================

if st.session_state.papers:
    st.subheader("📄 Retrieved Papers")

    for p in st.session_state.papers:
        st.markdown(f"**{p['title']}**")
        st.write(p["abstract"][:300] + "...")
        st.divider()