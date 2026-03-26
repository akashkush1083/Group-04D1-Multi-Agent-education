"""
Multi-Agent Education System — Streamlit Web App
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run:
    streamlit run app.py
"""

import os
import json
import re
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page config (MUST be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="EduAgent AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

<style>
/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0d14 !important;
    color: #e8e3d8 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(251,191,36,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(16,185,129,0.05) 0%, transparent 60%),
        #0a0d14 !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }

.block-container {
    padding: 2.5rem 3rem 4rem !important;
    max-width: 1100px !important;
}

/* ── Header ── */
.edu-header {
    text-align: center;
    padding: 3rem 0 2.5rem;
    position: relative;
}
.edu-header .badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(251,191,36,0.12);
    border: 1px solid rgba(251,191,36,0.3);
    color: #fbbf24;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 100px;
    margin-bottom: 1.2rem;
}
.edu-header h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: clamp(2.4rem, 5vw, 3.8rem) !important;
    font-weight: 900 !important;
    color: #f5f0e8 !important;
    line-height: 1.1 !important;
    letter-spacing: -0.02em !important;
    margin: 0 !important;
}
.edu-header h1 span { color: #fbbf24; }
.edu-header p {
    color: #7a7566;
    font-size: 1rem;
    margin-top: 0.8rem;
    font-weight: 300;
    letter-spacing: 0.01em;
}

/* ── Divider ── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(251,191,36,0.2), transparent);
    margin: 2rem 0;
}

/* ── Section Labels ── */
.section-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #fbbf24;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(251,191,36,0.15);
}

/* ── Search Card ── */
.search-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.5rem;
}

/* ── Override Streamlit input ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #f5f0e8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(251,191,36,0.5) !important;
    box-shadow: 0 0 0 3px rgba(251,191,36,0.08) !important;
}
.stTextInput > div > div > input::placeholder { color: #4a4740 !important; }
.stTextInput label {
    color: #9a9080 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 400 !important;
    margin-bottom: 6px !important;
}

/* ── Streamlit Button ── */
.stButton > button {
    background: linear-gradient(135deg, #fbbf24, #f59e0b) !important;
    color: #0a0d14 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.03em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    transition: opacity 0.2s, transform 0.15s !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Agent status pills ── */
.agent-flow {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 1rem 0;
    flex-wrap: wrap;
}
.agent-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 100px;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.02em;
}
.pill-researcher {
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.3);
    color: #10b981;
}
.pill-writer {
    background: rgba(251,191,36,0.12);
    border: 1px solid rgba(251,191,36,0.3);
    color: #fbbf24;
}
.pill-arrow { color: #4a4740; font-size: 1rem; }

/* ── Result box ── */
.result-wrapper {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-left: 3px solid #fbbf24;
    border-radius: 0 14px 14px 0;
    padding: 2rem 2.2rem;
    margin-top: 1.5rem;
}
.result-meta {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 1.2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.result-topic-pill {
    background: rgba(251,191,36,0.15);
    border: 1px solid rgba(251,191,36,0.25);
    color: #fbbf24;
    padding: 3px 12px;
    border-radius: 100px;
    font-size: 0.78rem;
    font-weight: 500;
}
.result-time {
    color: #4a4740;
    font-size: 0.75rem;
}

/* ── Markdown output inside result ── */
.result-wrapper h1, .result-wrapper h2, .result-wrapper h3 {
    font-family: 'Playfair Display', serif !important;
    color: #f5f0e8 !important;
}
.result-wrapper p { color: #c8c0b0 !important; line-height: 1.75 !important; }
.result-wrapper ul, .result-wrapper ol { color: #c8c0b0 !important; }
.result-wrapper strong { color: #fbbf24 !important; }
.result-wrapper code {
    background: rgba(251,191,36,0.1) !important;
    color: #fbbf24 !important;
    border-radius: 4px !important;
    padding: 1px 5px !important;
}

/* ── History section ── */
.history-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}

/* ── History card ── */
.history-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s, background 0.2s;
    cursor: pointer;
}
.history-card:hover {
    border-color: rgba(251,191,36,0.25);
    background: rgba(251,191,36,0.04);
}
.history-card-top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 10px;
}
.history-topic {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #f5f0e8;
    line-height: 1.3;
}
.history-time {
    color: #4a4740;
    font-size: 0.72rem;
    white-space: nowrap;
    margin-top: 2px;
}
.history-preview {
    color: #5a5548;
    font-size: 0.82rem;
    margin-top: 6px;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.history-empty {
    text-align: center;
    padding: 3rem 2rem;
    color: #3a3530;
}
.history-empty .icon { font-size: 2.5rem; margin-bottom: 0.8rem; }
.history-empty p { font-size: 0.88rem; line-height: 1.6; }

/* ── Expander override ── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    margin-bottom: 0.8rem !important;
}
[data-testid="stExpander"] summary {
    color: #f5f0e8 !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    padding: 0.9rem 1.2rem !important;
}
[data-testid="stExpander"] summary:hover {
    background: rgba(251,191,36,0.04) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] > div {
    border-top-color: #fbbf24 !important;
}

/* ── Success / info / warning ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(251,191,36,0.2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(251,191,36,0.4); }

/* ── Column gap ── */
[data-testid="column"] { padding: 0 0.8rem !important; }
</style>
""", unsafe_allow_html=True)

# ── History helpers ────────────────────────────────────────────────────────────
HISTORY_FILE = "outputs/history.json"


def load_history() -> list:
    os.makedirs("outputs", exist_ok=True)
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_to_history(topic: str, result: str):
    history = load_history()
    entry = {
        "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "topic": topic,
        "result": str(result),
        "timestamp": datetime.now().strftime("%B %d, %Y  %H:%M"),
        "preview": str(result)[:180].strip().replace("\n", " "),
    }
    history.insert(0, entry)          # newest first
    history = history[:30]            # keep last 30
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

    # Also save individual .md file
    safe = re.sub(r"[^\w\s-]", "", topic.lower())
    safe = re.sub(r"\s+", "_", safe).strip("_")[:60]
    md_path = f"outputs/{safe}_{entry['id']}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Educational Study Guide: {topic}\n")
        f.write(f"*Generated on {entry['timestamp']}*\n\n---\n\n")
        f.write(str(result))


def delete_history_entry(entry_id: str):
    history = load_history()
    history = [h for h in history if h["id"] != entry_id]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


# ── Session state ──────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "result_topic" not in st.session_state:
    st.session_state.result_topic = ""
if "result_time" not in st.session_state:
    st.session_state.result_time = ""
if "selected_history" not in st.session_state:
    st.session_state.selected_history = None

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="edu-header">
    <div class="badge">🎓 Multi-Agent Education System</div>
    <h1>Learn Anything with <span>AI Agents</span></h1>
    <p>Researcher Agent sources the knowledge · Writer Agent crafts your study guide</p>
</div>
""", unsafe_allow_html=True)

# ── Two-column layout ──────────────────────────────────────────────────────────
left_col, right_col = st.columns([3, 2], gap="large")

# ═══════════════════════════════════════════════════════════════════════════════
# LEFT COLUMN — Search + Result
# ═══════════════════════════════════════════════════════════════════════════════
with left_col:

    # Section label
    st.markdown('<div class="section-label">🔍 &nbsp;Generate Study Guide</div>', unsafe_allow_html=True)

    # Search card
    with st.container():
        topic_input = st.text_input(
            "Enter an educational topic",
            placeholder="e.g. Photosynthesis, Newton's Laws, Machine Learning...",
            key="topic_input",
            label_visibility="visible",
        )

        # Agent flow pills
        st.markdown("""
        <div class="agent-flow">
            <span class="agent-pill pill-researcher">🔬 Researcher Agent</span>
            <span class="pill-arrow">→</span>
            <span class="agent-pill pill-writer">✍️ Writer Agent</span>
        </div>
        """, unsafe_allow_html=True)

        generate_btn = st.button("Generate Study Guide  ✦", key="generate")

    # ── Run agents ────────────────────────────────────────────────────────────
    if generate_btn:
        if not topic_input.strip():
            st.warning("Please enter a topic before generating.")
        else:
            # Import here so Streamlit doesn't hang on module load
            try:
                from crew_setup import crew
            except Exception as e:
                st.error(f"Failed to load agents: {e}")
                st.stop()

            with st.spinner(f"Agents are working on **{topic_input}** …"):
                try:
                    result = crew.kickoff(inputs={"topic": topic_input.strip()})
                    st.session_state.result = result
                    st.session_state.result_topic = topic_input.strip()
                    st.session_state.result_time = datetime.now().strftime("%B %d, %Y  %H:%M")
                    st.session_state.selected_history = None  # clear history view

                    # Persist to history
                    save_to_history(topic_input.strip(), result)
                    st.success("Study guide generated and saved to history!")

                except Exception as e:
                    st.error(f"Agent error: {e}")

    # ── Display result ─────────────────────────────────────────────────────────
    active_result = st.session_state.selected_history or (
        {"topic": st.session_state.result_topic,
         "result": st.session_state.result,
         "timestamp": st.session_state.result_time}
        if st.session_state.result else None
    )

    if active_result and active_result.get("result"):
        st.markdown(f"""
        <div class="result-meta" style="margin-top:1.5rem;">
            <span class="result-topic-pill">📘 {active_result['topic']}</span>
            <span class="result-time">{active_result.get('timestamp','')}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            f'<div style="border-left: 3px solid #fbbf24; padding-left: 1.2rem; margin-top:0.5rem;">',
            unsafe_allow_html=True
        )
        st.markdown(str(active_result["result"]))
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="text-align:center; padding:4rem 2rem; color:#3a3530;">
            <div style="font-size:3rem;margin-bottom:1rem;">📖</div>
            <p style="font-size:0.9rem;line-height:1.7;color:#4a4740;">
                Enter a topic above and click <strong style="color:#fbbf24">Generate Study Guide</strong>.<br>
                Your personalised educational content will appear here.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# RIGHT COLUMN — History
# ═══════════════════════════════════════════════════════════════════════════════
with right_col:

    history = load_history()

    # Header row
    h_col1, h_col2 = st.columns([3, 1])
    with h_col1:
        st.markdown(
            f'<div class="section-label">🕒 &nbsp;Saved History &nbsp;<span style="color:#4a4740;font-size:0.65rem;letter-spacing:0.05em;">({len(history)} guides)</span></div>',
            unsafe_allow_html=True
        )
    with h_col2:
        if history:
            if st.button("Clear All", key="clear_all"):
                if os.path.exists(HISTORY_FILE):
                    os.remove(HISTORY_FILE)
                st.session_state.selected_history = None
                st.rerun()

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    if not history:
        st.markdown("""
        <div class="history-empty">
            <div class="icon">📂</div>
            <p>No saved guides yet.<br>Generate your first study guide<br>to see it here.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for entry in history:
            with st.expander(f"📘 {entry['topic']}", expanded=False):

                # Metadata row
                st.markdown(
                    f'<p style="font-size:0.72rem;color:#4a4740;margin-bottom:0.8rem;">🕒 {entry["timestamp"]}</p>',
                    unsafe_allow_html=True
                )

                btn_col1, btn_col2 = st.columns([1, 1])
                with btn_col1:
                    if st.button("View Guide", key=f"view_{entry['id']}"):
                        st.session_state.selected_history = entry
                        st.session_state.result = None
                        st.rerun()
                with btn_col2:
                    if st.button("🗑 Delete", key=f"del_{entry['id']}"):
                        delete_history_entry(entry["id"])
                        if (st.session_state.selected_history and
                                st.session_state.selected_history.get("id") == entry["id"]):
                            st.session_state.selected_history = None
                        st.rerun()

                # Preview snippet
                if entry.get("preview"):
                    st.markdown(
                        f'<p style="font-size:0.8rem;color:#5a5548;margin-top:0.5rem;line-height:1.5;">'
                        f'{entry["preview"]}…</p>',
                        unsafe_allow_html=True
                    )

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-divider" style="margin-top:3rem;"></div>', unsafe_allow_html=True)
st.markdown("""
<p style="text-align:center;font-size:0.72rem;color:#2a2520;padding-bottom:1rem;letter-spacing:0.05em;">
    MULTI-AGENT EDUCATION SYSTEM &nbsp;·&nbsp; CREWAI + GROQ LLAMA 3.1 &nbsp;·&nbsp; RESEARCHER → WRITER
</p>
""", unsafe_allow_html=True)
