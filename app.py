# app.py
import streamlit as st
from chatbot import SimpleChatbot
from sentiment_statement import analyze_statement
from sentiment_conversation import analyze_conversation_with_gemini

st.set_page_config(page_title="LiaPlus Chatbot", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
        .chat-bubble-user {
            background-color: #534B4F;
            padding: 10px 15px;
            border-radius: 15px;
            margin-bottom: 8px;
            max-width: 80%;
            float: right;
            clear: both;
        }
        .chat-bubble-bot {
            background-color: #483C32;
            padding: 10px 15px;
            border-radius: 15px;
            margin-bottom: 8px;
            max-width: 80%;
            float: left;
            clear: both;
        }
        .tier-card {
            padding: 15px;
            background: #494F5F;
            border-radius: 10px;
            border: 1px solid #ddd;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "bot" not in st.session_state:
    st.session_state.bot = SimpleChatbot()

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""


st.title("💬 LiaPlus Chatbot")
st.caption("Chat with the bot. Type `/end` to get full conversation sentiment.")

# ---------- MESSAGE INPUT FORM ----------
with st.form(key="chat_form", clear_on_submit=True):
    user_msg = st.text_input("Message:", placeholder="Type your message…", key="input_text")
    submitted = st.form_submit_button("Send")

# ---------- PROCESS USER MESSAGE ----------
if submitted and user_msg:
    # /end command logic
    if user_msg.strip().lower() == "/end":
        st.subheader("📝 Statement-level Sentiment (Tier 2)")

        user_msgs = st.session_state.bot.get_user_messages()
        for i, msg in enumerate(user_msgs, start=1):
            res = analyze_statement(msg)
            st.markdown(
                f"""
                <div class="tier-card">
                    <b>{i:02}. {msg}</b><br>
                    Sentiment: <b>{res['label']}</b><br>
                    Score: {res['score']:.3f}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("---")

        st.subheader("📌 Conversation-level Sentiment (Tier 1)")
        conv_text = st.session_state.bot.as_text(include_bot=True)
        summary = analyze_conversation_with_gemini(conv_text, use_gemini=True)

        # Pretty summary card
        st.markdown(
            f"""
            <div class="tier-card">
                <h4>Overall Sentiment: {summary['overall_label']}</h4>
                <p><b>Average Score:</b> {summary['average_score']}</p>
                <p><b>Trend:</b> {summary['trend']}</p>
                <p><b>Confidence:</b> {summary['confidence']}</p>
                <p><b>Reason:</b> {summary['reason']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.warning("Conversation ended. Refresh the page to start again.")

    else:
        # Regular chatbot reply
        reply = st.session_state.bot.handle_user(user_msg)
        st.session_state.chat_log.append(("User", user_msg))
        st.session_state.chat_log.append(("Bot", reply))


# ---------- CHAT DISPLAY ----------
st.subheader("💭 Conversation")

for speaker, msg in st.session_state.chat_log:
    if speaker == "User":
        st.markdown(f'<div class="chat-bubble-user">🧑 <b>You:</b> {msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-bot">🤖 <b>Bot:</b> {msg}</div>', unsafe_allow_html=True)

st.write("")  # spacing
