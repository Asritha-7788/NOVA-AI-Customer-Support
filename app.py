
import streamlit as st
import hashlib

from chatbot import get_response
from sentiment import analyze_sentiment
from voice import speech_to_text, text_to_speech


# =============== PAGE CONFIG ===============

st.set_page_config(
    page_title="NOVA | AI Support",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =============== SESSION STATE ===============

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None

if "last_sentiment" not in st.session_state:
    st.session_state.last_sentiment = {
        "sentiment": "Waiting",
        "emoji": "💬",
        "score": 0
    }

if "last_error" not in st.session_state:
    st.session_state.last_error = None


def process_message(user_message):

    if not user_message.strip():
        return

    st.session_state.last_error = None

    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    st.session_state.last_sentiment = analyze_sentiment(
        user_message
    )

    try:
        with st.spinner("NOVA is thinking..."):
            reply = get_response(st.session_state.messages)

        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })

    except Exception as e:
        st.session_state.last_error = str(e)


# =============== CUSTOM DESIGN ===============

st.markdown("""
<style>

/* REMOVE WHITE BACKGROUNDS EVERYWHERE */

html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main,
[data-testid="stMainBlockContainer"] {
    background: #080d19 !important;
    color: #e5e7eb !important;
}

header[data-testid="stHeader"] {
    background: #080d19 !important;
}

[data-testid="stToolbar"] {
    background: transparent !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

footer {
    background: #080d19 !important;
    color: #64748b !important;
}

[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"] {
    background: #080d19 !important;
}

[data-testid="stChatInput"] {
    background: #111b30 !important;
    border: 1px solid #344563 !important;
    border-radius: 14px !important;
}

[data-testid="stChatInput"] textarea {
    color: white !important;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #0c1425 !important;
    border-right: 1px solid #202d45;
}

section[data-testid="stSidebar"] * {
    color: #dbeafe;
}

.sidebar-logo {
    font-size: 32px;
    font-weight: 900;
    letter-spacing: 2px;
    color: #a5b4fc !important;
}

.sidebar-subtitle {
    font-size: 10px;
    letter-spacing: 2px;
    color: #64748b !important;
}

.feature-item {
    background: #131f35;
    border: 1px solid #24344e;
    border-radius: 10px;
    padding: 12px;
    margin: 9px 0;
    color: #cbd5e1;
    font-size: 13px;
}

/* HERO HEADER */

.hero {
    background:
        radial-gradient(circle at 85% 20%, #4338ca 0%, transparent 35%),
        linear-gradient(115deg, #111d38, #171b43 65%, #25205a);
    border: 1px solid #393b78;
    border-radius: 22px;
    padding: 30px;
    margin-bottom: 25px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.25);
}

.hero-label {
    color: #a5b4fc;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
}

.hero-title {
    font-size: 34px;
    line-height: 1.3;
    font-weight: 800;
    color: #ffffff !important;
    margin: 10px 0;
}

.hero-description {
    color: #b7c4dc !important;
    font-size: 14px;
}

.online-status {
    display: inline-block;
    color: #86efac !important;
    background: #12352d;
    padding: 7px 13px;
    border-radius: 30px;
    font-size: 12px;
    margin-top: 12px;
}

/* DASHBOARD CARDS */

.dashboard-card {
    background: linear-gradient(145deg, #15223a, #101a2d);
    border: 1px solid #273956;
    border-radius: 17px;
    padding: 20px;
    min-height: 135px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.15);
}

.card-icon {
    font-size: 22px;
}

.card-label {
    color: #94a3b8 !important;
    font-size: 12px;
    margin-top: 12px;
}

.card-value {
    color: #f8fafc !important;
    font-size: 27px;
    font-weight: 800;
    margin-top: 5px;
}

.card-note {
    color: #818cf8 !important;
    font-size: 11px;
    margin-top: 5px;
}

/* SECTION TITLES */

.section-title {
    color: #f1f5f9 !important;
    font-size: 19px;
    font-weight: 750;
    margin: 15px 0;
}

/* PANELS */

.panel {
    background: #101a2d;
    border: 1px solid #263650;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 15px;
}

.panel-heading {
    color: #e2e8f0 !important;
    font-size: 17px;
    font-weight: 750;
}

.panel-description {
    color: #94a3b8 !important;
    font-size: 12px;
}

/* CHAT AREA */

div[data-testid="stChatMessage"] {
    background: #17243a !important;
    border: 1px solid #293b58 !important;
    border-radius: 15px !important;
    padding: 15px !important;
    margin-bottom: 12px;
}

div[data-testid="stChatMessage"] p {
    color: #e2e8f0 !important;
}

div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
    color: #e2e8f0 !important;
}

/* BUTTONS */

.stButton > button {
    background: linear-gradient(110deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 650 !important;
    padding: 10px 15px !important;
    min-height: 42px;
}

.stButton > button:hover {
    background: linear-gradient(110deg, #6366f1, #8b5cf6) !important;
    transform: translateY(-1px);
}

/* VOICE PANEL */

.voice-card {
    background:
        radial-gradient(circle at 90% 20%, #3730a3 0%, transparent 45%),
        linear-gradient(135deg, #17233c, #151b3d);
    border: 1px solid #41458a;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 12px;
}

.voice-title {
    color: #e0e7ff !important;
    font-size: 18px;
    font-weight: 750;
}

.voice-description {
    color: #a5b4fc !important;
    font-size: 12px;
}

/* INSIGHT CARDS */

.insight-card {
    background: #152239;
    border: 1px solid #2c3d59;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 12px;
}

.insight-label {
    color: #94a3b8 !important;
    font-size: 11px;
    letter-spacing: 1px;
}

.insight-value {
    color: #f8fafc !important;
    font-size: 21px;
    font-weight: 750;
    margin-top: 7px;
}

/* INPUT WIDGETS */

[data-testid="stAudioInput"] {
    background: #17243a !important;
    border: 1px solid #344563 !important;
    border-radius: 12px;
    padding: 12px;
}

[data-testid="stAudioInput"] * {
    color: #e2e8f0 !important;
}

/* DIVIDERS */

hr {
    border-color: #25334c !important;
}

/* FOOTER */

.custom-footer {
    text-align: center;
    padding: 25px 10px;
    color: #64748b !important;
    font-size: 11px;
    border-top: 1px solid #202d45;
    margin-top: 35px;
}

</style>
""", unsafe_allow_html=True)


# =============== SIDEBAR ===============

with st.sidebar:

    st.markdown(
        '<div class="sidebar-logo">✦ NOVA</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">AI CUSTOMER INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### Workspace")

    if st.button("＋ New Conversation", use_container_width=True):

        st.session_state.messages = []
        st.session_state.last_sentiment = {
            "sentiment": "Waiting",
            "emoji": "💬",
            "score": 0
        }
        st.session_state.last_audio_hash = None
        st.session_state.last_error = None
        st.rerun()

    st.markdown("### AI Capabilities")

    for item in [
        "🤖  Intelligent AI Chat",
        "💭  Emotion Detection",
        "🧠  Contextual Memory",
        "🎙️  Speech Recognition",
        "🔊  Voice Generation"
    ]:
        st.markdown(
            f'<div class="feature-item">{item}</div>',
            unsafe_allow_html=True
        )

    st.divider()

    st.markdown("### System")

    st.markdown(
        '<div style="color:#86efac;font-size:13px;">'
        '● Assistant interface active</div>',
        unsafe_allow_html=True
    )

    st.caption("Gemini AI · Python · NLP")


# =============== HERO ===============

st.markdown("""
<div class="hero">
    <div class="hero-label">✦ YOUR INTELLIGENT SUPPORT WORKSPACE</div>
    <div class="hero-title">Customer support,<br>reimagined with AI.</div>
    <div class="hero-description">
        Meet NOVA — an intelligent assistant that understands,
        responds and communicates through text and voice.
    </div>
    <div class="online-status">● SYSTEM ONLINE</div>
</div>
""", unsafe_allow_html=True)


# =============== DASHBOARD ===============

st.markdown(
    '<div class="section-title">◈ Dashboard Overview</div>',
    unsafe_allow_html=True
)

total_messages = len(st.session_state.messages)
user_count = sum(
    1 for m in st.session_state.messages if m["role"] == "user"
)
assistant_count = sum(
    1 for m in st.session_state.messages if m["role"] == "assistant"
)

sentiment = st.session_state.last_sentiment

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="dashboard-card">
        <div class="card-icon">💬</div>
        <div class="card-label">TOTAL MESSAGES</div>
        <div class="card-value">{total_messages}</div>
        <div class="card-note">Messages in this session</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="dashboard-card">
        <div class="card-icon">👤</div>
        <div class="card-label">CUSTOMER MESSAGES</div>
        <div class="card-value">{user_count}</div>
        <div class="card-note">Incoming interactions</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="dashboard-card">
        <div class="card-icon">🤖</div>
        <div class="card-label">AI RESPONSES</div>
        <div class="card-value">{assistant_count}</div>
        <div class="card-note">Generated responses</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="dashboard-card">
        <div class="card-icon">{sentiment['emoji']}</div>
        <div class="card-label">LATEST SENTIMENT</div>
        <div class="card-value" style="font-size:22px;">
            {sentiment['sentiment']}
        </div>
        <div class="card-note">Customer emotion analysis</div>
    </div>
    """, unsafe_allow_html=True)


# =============== MAIN TWO-COLUMN LAYOUT ===============

st.markdown("")

chat_col, insight_col = st.columns([1.85, 1], gap="large")


# =============== CHAT INTERFACE ===============

with chat_col:

    st.markdown("""
    <div class="panel">
        <div class="panel-heading">💬 AI Conversation</div>
        <div class="panel-description">
            Chat with NOVA for instant customer support.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.messages:

        st.markdown("""
        <div class="panel" style="text-align:center;padding:40px 15px;">
            <div style="font-size:45px;">✦</div>
            <div style="font-size:20px;font-weight:750;color:#e0e7ff;">
                Welcome to NOVA
            </div>
            <p style="color:#94a3b8;font-size:13px;">
                Your conversation starts here.
                Ask a question about orders, payments,
                refunds or customer service.
            </p>
        </div>
        """, unsafe_allow_html=True)

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])

            if message["role"] == "user":

                result = analyze_sentiment(message["content"])

                st.caption(
                    f"{result['emoji']} {result['sentiment']} "
                    f"sentiment · Score {result['score']:.2f}"
                )

    user_input = st.chat_input(
        "Message NOVA... Type your question"
    )

    if user_input:
        process_message(user_input)
        st.rerun()


# =============== INTELLIGENCE PANEL ===============

with insight_col:

    st.markdown("""
    <div class="panel-heading">◈ Customer Intelligence</div>
    <div class="panel-description">
        Live analysis of the current conversation
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-label">CUSTOMER SENTIMENT</div>
        <div class="insight-value">
            {sentiment['emoji']} {sentiment['sentiment']}
        </div>
        <div class="panel-description">
            Sentiment score: {sentiment['score']:.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-label">CONVERSATION MEMORY</div>
        <div class="insight-value">
            {'🟢 Active' if total_messages else '⚪ Waiting'}
        </div>
        <div class="panel-description">
            Current session conversation history
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-label">INTERACTION BREAKDOWN</div>
        <div style="color:#cbd5e1;font-size:13px;margin-top:10px;">
            Customer messages: <b>{user_count}</b>
        </div>
        <div style="color:#cbd5e1;font-size:13px;margin-top:8px;">
            AI responses: <b>{assistant_count}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="voice-card">
        <div class="voice-title">🎙️ Voice Assistant</div>
        <div class="voice-description">
            Speak naturally. NOVA will transcribe
            your voice and respond.
        </div>
    </div>
    """, unsafe_allow_html=True)

    audio = st.audio_input("Record your message")

    if audio is not None:

        audio_bytes = audio.getvalue()
        audio_hash = hashlib.sha256(audio_bytes).hexdigest()

        if audio_hash != st.session_state.last_audio_hash:

            st.session_state.last_audio_hash = audio_hash

            with st.spinner("Transcribing your voice..."):

                try:
                    transcribed_text = speech_to_text(audio_bytes)

                    if transcribed_text:
                        st.success(f"You said: {transcribed_text}")
                        process_message(transcribed_text)
                        st.rerun()
                    else:
                        st.warning("No speech detected.")

                except Exception as e:
                    st.error(f"Voice recognition error: {e}")

    if (
        st.session_state.messages
        and st.session_state.messages[-1]["role"] == "assistant"
    ):

        st.markdown(
            '<div class="panel-heading" style="margin-top:20px;">'
            '🔊 AI Voice Response</div>',
            unsafe_allow_html=True
        )

        if st.button("▶ Generate Voice", use_container_width=True):

            with st.spinner("Generating audio..."):

                try:
                    audio_buffer = text_to_speech(
                        st.session_state.messages[-1]["content"]
                    )

                    st.audio(audio_buffer, format="audio/mp3")

                except Exception as e:
                    st.error(f"Voice generation error: {e}")


# =============== ERROR DISPLAY ===============

if st.session_state.last_error:
    st.error(
        "AI response error: " + st.session_state.last_error
    )


# =============== FOOTER ===============

st.markdown("""
<div class="custom-footer">
    ✦ NOVA AI CUSTOMER SUPPORT ASSISTANT
    <br><br>
    Built with Python · Streamlit · Gemini AI · NLP
</div>
""", unsafe_allow_html=True)
