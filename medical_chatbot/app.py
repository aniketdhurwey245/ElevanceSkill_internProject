import streamlit as st
import pandas as pd
import time
from datetime import datetime
from typing import Optional   
 
# ── Page config 
st.set_page_config(
    page_title="MedChat · Medical Q&A",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "MedChat: AI-powered Medical Q&A using the MedQuAD dataset.",
    },
)
 
# ── Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');
 
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
 
/* ── Color tokens ── */
:root {
    --bg-primary:    #0d1117;
    --bg-card:       #161b22;
    --bg-surface:    #1c2128;
    --accent:        #00c8a0;
    --accent2:       #0070f3;
    --danger:        #ff6b6b;
    --warn:          #ffa94d;
    --text-primary:  #e6edf3;
    --text-secondary:#8b949e;
    --border:        #30363d;
}
 
/* ── Global overrides ── */
.stApp { background: var(--bg-primary); }
.block-container { padding: 1.5rem 2rem; max-width: 1200px; }
 
/* ── Hero header ── */
.hero-header {
    background: linear-gradient(135deg, #0d1117 0%, #0a2540 50%, #0d1117 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(0,200,160,0.07) 0%, transparent 60%),
                radial-gradient(circle at 70% 30%, rgba(0,112,243,0.07) 0%, transparent 60%);
    pointer-events: none;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    color: var(--text-primary);
    margin: 0 0 0.3rem;
    line-height: 1.2;
}
.hero-title span { color: var(--accent); }
.hero-subtitle {
    color: var(--text-secondary);
    font-size: 1rem;
    margin: 0;
}
 
/* ── Chat message bubbles ── */
.chat-msg-user {
    background: linear-gradient(135deg, #0070f3, #005fcc);
    border-radius: 16px 16px 4px 16px;
    padding: 0.9rem 1.2rem;
    margin: 0.5rem 0 0.5rem 15%;
    color: #fff;
    font-size: 0.95rem;
    box-shadow: 0 2px 12px rgba(0,112,243,0.25);
}
.chat-msg-bot {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 4px 16px 16px 16px;
    padding: 1.1rem 1.3rem;
    margin: 0.5rem 15% 0.5rem 0;
    color: var(--text-primary);
    font-size: 0.93rem;
    line-height: 1.65;
}
.chat-msg-meta {
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin-top: 0.5rem;
    padding-top: 0.5rem;
    border-top: 1px solid var(--border);
}
.chat-timestamp {
    font-size: 0.72rem;
    color: var(--text-secondary);
    text-align: right;
    margin-top: 0.2rem;
}
 
/* ── Confidence badge ── */
.confidence-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.78rem;
    padding: 3px 10px;
    border-radius: 20px;
    font-weight: 600;
    margin-bottom: 0.6rem;
}
.conf-high   { background: rgba(105,219,124,0.15); color: #69db7c; border: 1px solid rgba(105,219,124,0.3); }
.conf-med    { background: rgba(255,169,77,0.15);  color: #ffa94d; border: 1px solid rgba(255,169,77,0.3);  }
.conf-low    { background: rgba(255,107,107,0.15); color: #ff6b6b; border: 1px solid rgba(255,107,107,0.3); }
 
/* ── Entity tags ── */
.entity-section { margin: 0.8rem 0; }
.entity-section-title {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-secondary);
    margin-bottom: 0.4rem;
}
.entity-tag {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.76rem;
    font-weight: 600;
    margin: 2px 3px;
}
 
/* ── Stat cards ── */
.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.stat-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--accent);
    line-height: 1;
}
.stat-label {
    font-size: 0.78rem;
    color: var(--text-secondary);
    margin-top: 0.3rem;
}
 
/* ── Suggested pills ── */
.suggested-chip {
    display: inline-block;
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.82rem;
    color: var(--text-secondary);
    margin: 0.2rem;
    cursor: pointer;
    transition: all 0.2s;
}
.suggested-chip:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: rgba(0,200,160,0.07);
}
 
/* ── Disclaimer box ── */
.disclaimer-box {
    background: rgba(255,169,77,0.08);
    border: 1px solid rgba(255,169,77,0.2);
    border-radius: 8px;
    padding: 0.7rem 1rem;
    font-size: 0.8rem;
    color: #ffa94d;
    margin-top: 0.8rem;
}
 
/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .stMarkdown { color: var(--text-primary); }
 
/* ── Input styling ── */
.stTextInput>div>div>input {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    padding: 0.7rem 1rem !important;
    font-size: 0.95rem !important;
}
.stTextInput>div>div>input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,200,160,0.15) !important;
}
 
/* ── Button styling ── */
.stButton>button {
    background: linear-gradient(135deg, var(--accent), #00a87e) !important;
    color: #0d1117 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.5rem !important;
    font-size: 0.9rem !important;
    transition: all 0.2s !important;
}
.stButton>button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(0,200,160,0.3) !important;
}
 
/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1rem 0 !important; }
 
/* ── No scroll flicker ── */
.main .block-container { overflow: visible; }
</style>
""", unsafe_allow_html=True)
 
 
# ── Session State Init ────────────────────────────────────────────────────────
def _init_state():
    defaults = {
        "messages":       [],
        "retriever":      None,
        "df":             None,
        "ner":            None,
        "system_ready":   False,
        "stats":          {},
        "query_count":    0,
        "loading":        False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
 
_init_state()
 
 
# ── Load & Cache Resources ────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def _load_system():
    """Load data + build index. Cached across sessions."""
    from utils.data_loader import load_medquad_data, get_dataset_stats
    from utils.retrieval_engine import MedicalQARetriever
    from utils.entity_recognizer import MedicalEntityRecognizer
 
    df = load_medquad_data(
        cache_path="data/medquad_cache.json",
        max_files_per_folder=8,
        use_cache=True,
    )
    stats = get_dataset_stats(df)
 
    retriever = MedicalQARetriever(index_path="data/retrieval_index.pkl")
    if not retriever.load_index():
        retriever.build_index(df, save=True)
 
    ner = MedicalEntityRecognizer()
    return retriever, ner, df, stats
 
 
def _ensure_system_loaded():
    if not st.session_state.system_ready:
        with st.spinner("🩺 Loading MedQuAD dataset and building search index..."):
            retriever, ner, df, stats = _load_system()
            st.session_state.retriever  = retriever
            st.session_state.ner        = ner
            st.session_state.df         = df
            st.session_state.stats      = stats
            st.session_state.system_ready = True
 
 
# ── Helpers ───────────────────────────────────────────────────────────────────
def _get_confidence_class(label: str) -> str:
    if "High"     in label: return "conf-high"
    if "Moderate" in label: return "conf-med"
    return "conf-low"
 
 
def _render_entity_tags(entities: dict) -> str:
    from utils.entity_recognizer import LABEL_COLORS, LABEL_ICONS
    if not entities:
        return ""
    html_parts = ['<div class="entity-section"><div class="entity-section-title">🔍 Detected Medical Entities</div>']
    for label, terms in entities.items():
        color = LABEL_COLORS.get(label, "#888")
        icon  = LABEL_ICONS.get(label, "")
        for term in terms[:5]:   # max 5 per category
            html_parts.append(
                f'<span class="entity-tag" style="background:{color}18;'
                f'color:{color};border:1px solid {color}40;">'
                f'{icon} {term}</span>'
            )
    html_parts.append("</div>")
    return "".join(html_parts)
 
 
def _process_query(query: str, top_k: int, q_type_filter: Optional[str]) -> dict:
    from utils.response_formatter import format_primary_response, format_alternative_results

    retriever: MedicalQARetriever = st.session_state.retriever
    ner: MedicalEntityRecognizer = st.session_state.ner

    #  1. Normalize query
    query = query.lower().strip()

    #  2. Improve short queries
    if len(query.split()) < 3:
        query += " disease symptoms treatment"

    #  3. Retrieve results
    results = retriever.retrieve(
        query,
        top_k=max(top_k, 5),  # ensure enough results for diversity
        question_type_filter=q_type_filter if q_type_filter != "All" else None,
    )

    #  4. Prevent repeated answers
    last_answer = None
    if st.session_state.messages:
        last_msg = st.session_state.messages[-1]
        if last_msg["role"] == "assistant":
            last_answer = last_msg.get("content")

    if results and last_answer:
        # Remove repeated answer
        results = [r for r in results if r.answer != last_answer]

    #  5. Fallback if all filtered
    if not results:
        results = retriever.retrieve(query, top_k=top_k)

    #  6. Add slight randomness (top 3)
    import random
    if len(results) > 2:
        results = sorted(results, key=lambda x: x.score, reverse=True)
        results[0] = random.choice(results[:3])

    #  7. Format response
    formatted = format_primary_response(results)
    alternatives = format_alternative_results(results)

    #  8. Entity detection
    entities = ner.get_entity_summary(query + " " + formatted.get("answer", ""))

    return {
        **formatted,
        "alternatives": alternatives,
        "entities": entities,
        "query": query,
        "timestamp": datetime.now().strftime("%H:%M"),
    }
 
# ── Sidebar 
def _render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding:1rem 0 0.5rem;">
            <div style="font-size:1.4rem;font-weight:700;color:#e6edf3;">🩺 MedChat</div>
            <div style="font-size:0.8rem;color:#8b949e;">Powered by MedQuAD Dataset</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
 
        # ── Dataset stats ──
        st.markdown("**📊 Dataset Statistics**")
        stats = st.session_state.stats
        if stats:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""<div class="stat-card">
                    <div class="stat-value">{stats.get('total_qa_pairs', 0):,}</div>
                    <div class="stat-label">QA Pairs</div></div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""<div class="stat-card">
                    <div class="stat-value">{stats.get('unique_topics', 0):,}</div>
                    <div class="stat-label">Topics</div></div>""", unsafe_allow_html=True)
 
        st.markdown("---")
 
        # ── Search settings ──
        st.markdown("**⚙️ Search Settings**")
        top_k = st.slider("Results to retrieve", 1, 10, 3)
        q_type = st.selectbox(
            "Filter by question type",
            ["All", "Information", "Symptoms", "Treatment", "Causes",
             "Diagnosis", "Prevention", "Prognosis"],
        )
 
        st.markdown("---")
 
        # ── Entity legend ──
        st.markdown("**🏷️ Entity Legend**")
        from utils.entity_recognizer import LABEL_COLORS, LABEL_ICONS
        for label, color in LABEL_COLORS.items():
            icon = LABEL_ICONS.get(label, "")
            st.markdown(
                f'<span style="background:{color}20;color:{color};border:1px solid {color}50;'
                f'border-radius:12px;padding:2px 10px;font-size:0.8rem;font-weight:600;">'
                f'{icon} {label}</span> ',
                unsafe_allow_html=True
            )
 
        st.markdown("---")
 
        # ── Clear chat ──
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.session_state.query_count = 0
            st.rerun()
 
        # ── Session info ──
        st.markdown(f"""
        <div style="font-size:0.75rem;color:#8b949e;margin-top:1rem;">
            💬 Queries this session: <strong style="color:#e6edf3;">{st.session_state.query_count}</strong>
        </div>
        """, unsafe_allow_html=True)
 
    return top_k, q_type
 
 
# ── Chat Message Renderer ─────────────────────────────────────────────────────
def _render_message(msg: dict):
    role = msg["role"]
    ts   = msg.get("timestamp", "")
 
    if role == "user":
        st.markdown(
            f'<div class="chat-msg-user">{msg["content"]}'
            f'<div class="chat-timestamp">{ts}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        data = msg.get("data", {})
        conf_label   = data.get("confidence_label", "")
        conf_class   = _get_confidence_class(conf_label)
        conf_score   = data.get("confidence_score", 0)
        answer       = data.get("answer", msg.get("content", ""))
        metadata     = data.get("metadata", "")
        entities     = data.get("entities", {})
        alternatives = data.get("alternatives", [])
        disclaimer   = data.get("disclaimer", "")
        matched_q    = data.get("matched_question", "")
 
        # Confidence badge
        badge_html = (
            f'<span class="confidence-badge {conf_class}">'
            f'{conf_label} &nbsp;·&nbsp; {conf_score}%</span>'
            if conf_label else ""
        )
 
        # Matched question
        matched_html = (
            f'<div style="font-size:0.78rem;color:#8b949e;margin-bottom:0.6rem;">'
            f'📎 <em>Matched: {matched_q[:80]}{"…" if len(matched_q)>80 else ""}</em></div>'
            if matched_q else ""
        )
 
        # Entity tags
        entity_html = _render_entity_tags(entities)
 
        # Disclaimer
        disclaimer_html = (
            f'<div class="disclaimer-box">{disclaimer}</div>'
            if disclaimer else ""
        )
 
        # Metadata
        meta_html = (
            f'<div class="chat-msg-meta">{metadata}</div>'
            if metadata else ""
        )
 
        st.markdown(
            f'<div class="chat-msg-bot">'
            f'{badge_html}{matched_html}'
            f'<div style="margin:0.5rem 0 0.8rem;">{answer}</div>'
            f'{entity_html}{disclaimer_html}{meta_html}'
            f'<div class="chat-timestamp">{ts}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
 
        # Alternative results expander
        if alternatives:
            with st.expander(f"📚 {len(alternatives)} more related result(s)"):
                for alt in alternatives:
                    with st.container():
                        st.markdown(
                            f"**#{alt['rank']} · {alt['focus']}** "
                            f"<span style='color:#8b949e;font-size:0.8rem;'>"
                            f"({alt['confidence_label']} · {alt['score']}%)</span>",
                            unsafe_allow_html=True,
                        )
                        st.markdown(f"*Q: {alt['question']}*")
                        st.markdown(alt["answer"])
                        st.markdown("---")
 
 
# ── Suggested Queries ─────────────────────────────────────────────────────────
def _render_suggestions():
    from utils.response_formatter import get_suggested_topics
    suggestions = get_suggested_topics()
    st.markdown(
        '<div style="font-size:0.85rem;color:#8b949e;margin-bottom:0.5rem;">💡 Try asking:</div>',
        unsafe_allow_html=True,
    )
    cols = st.columns(4)
    for i, s in enumerate(suggestions[:8]):
        with cols[i % 4]:
            if st.button(s, key=f"sug_{i}", use_container_width=True):
                return s
    return None
 
 
# ── Main App ──────────────────────────────────────────────────────────────────
def main():
    _ensure_system_loaded()
    top_k, q_type = _render_sidebar()
 
    # ── Hero Header ──
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">🩺 Med<span>Chat</span></div>
        <div class="hero-subtitle">
            AI-powered medical question answering using the
            <strong style="color:#74c0fc;">MedQuAD</strong> dataset ·
            Retrieval-based · Entity-aware · Educational use only
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    # ── Render chat history ──
    if st.session_state.messages:
        for msg in st.session_state.messages:
            _render_message(msg)
    else:
        # Welcome card
        st.markdown("""
        <div style="background:#161b22;border:1px solid #30363d;border-radius:12px;
                    padding:1.5rem;margin:1rem 0;text-align:center;">
            <div style="font-size:2rem;margin-bottom:0.5rem;">👋</div>
            <div style="font-size:1.05rem;color:#e6edf3;font-weight:600;">
                Welcome to MedChat!
            </div>
            <div style="font-size:0.88rem;color:#8b949e;margin-top:0.4rem;">
                Ask me about diseases, symptoms, treatments, medications, or any medical topic.
                <br>I'll search the MedQuAD dataset to find the best answer.
            </div>
        </div>
        """, unsafe_allow_html=True)
 
    # ── Suggestion pills (only when chat is empty) ──
    if not st.session_state.messages:
        prefill = _render_suggestions()
        if prefill:
            st.session_state["_prefill"] = prefill
            st.rerun()
 
    st.markdown("---")
 
    # ── Input area ──
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        prefill_val = st.session_state.pop("_prefill", "")
        user_input = st.text_input(
            "Ask a medical question",
            value=prefill_val,
            placeholder="e.g. What are the symptoms of diabetes?",
            label_visibility="collapsed",
            key="main_input",
        )
    with col_btn:
        send_clicked = st.button("Send 🔍", use_container_width=True)
 
    # ── Process query ──
    if (send_clicked or user_input) and user_input.strip():
        query = user_input.strip()
 
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": query,
            "timestamp": datetime.now().strftime("%H:%M"),
        })
        st.session_state.query_count += 1
 
        # Process and add bot response
        with st.spinner("🔍 Searching medical knowledge base..."):
            result_data = _process_query(query, top_k, q_type)
 
        st.session_state.messages.append({
            "role": "assistant",
            "content": result_data.get("answer", ""),
            "data":    result_data,
            "timestamp": datetime.now().strftime("%H:%M"),
        })
        st.rerun()
 
 
if __name__ == "__main__":
    # Optional typing imports for type hints used in helpers
    from typing import Optional
    from utils.retrieval_engine import MedicalQARetriever
    from utils.entity_recognizer import MedicalEntityRecognizer
    main()
 