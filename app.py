import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# PAGE CONFIG
st.set_page_config(
    page_title="AI Movie Recommendation Agent",
    page_icon="🎬",
    layout="wide",
)

# CUSTOM CSS

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #777;
        margin-bottom: 30px;
    }

    .response-box {
        padding: 20px;
        border-radius: 12px;
        background-color: rgba(128, 128, 128, 0.08);
        margin-top: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# HEADER

st.markdown(
    '<div class="main-title">🎬 AI Movie Recommendation Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Ask about movies, discover similar films, or get personalized recommendations.'
    '</div>',
    unsafe_allow_html=True
)

# SIDEBAR

with st.sidebar:

    st.header("⚙️ Agent")

    st.markdown("### Available capabilities")

    st.write("🎥 Movie details")
    st.write("🔎 Similar movie recommendations")
    st.write("👤 Personalized recommendations")
    st.write("🎭 Genre-based recommendations")
    st.write("🤝 Collaborative recommendations")

    st.divider()

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()


# SESSION STATE

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = "streamlit_session"

st.sidebar.write(
    "Conversation ID:",
    st.session_state.conversation_id
)


# --------------------------------------------------
# DISPLAY PREVIOUS MESSAGES
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

user_input = st.chat_input(
    "Ask me something about movies..."
)


# --------------------------------------------------
# PROCESS REQUEST
# --------------------------------------------------

if user_input:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)


    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "conversation_id": st.session_state.conversation_id,
                        "message": user_input,
                    },
                    timeout=120,
                )

                response.raise_for_status()

                data = response.json()

                final_response = data.get(
                    "response",
                    "Sorry, I couldn't generate a response."
                )

                st.markdown(final_response)

                # Save response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": final_response
                    }
                )

            except Exception as e:

                error_message = f"Something went wrong: {e}"

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )