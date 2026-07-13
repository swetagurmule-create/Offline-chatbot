import streamlit as st
import google.generativeai as genai

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Offline AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# -------------------------------
# Load Gemini API Key
# -------------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("❌ Gemini API Key not found!")
    st.info("""
### How to fix

#### If running locally:
Create this file:

.streamlit/secrets.toml

Add:

GEMINI_API_KEY="YOUR_API_KEY"

#### If using Streamlit Cloud:
Manage App → Settings → Secrets

Add:

GEMINI_API_KEY="YOUR_API_KEY"
""")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# Load Model
model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------------
# Title
# -------------------------------
st.title("🤖 Offline AI Assistant")
st.caption("Powered by Google Gemini")

# -------------------------------
# Session State
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------
# Chat Input
# -------------------------------
prompt = st.chat_input("Type your question...")

if prompt:

    # User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = model.generate_content(
                    prompt + "\nAnswer in 2-3 lines only."
                )

                reply = response.text

            except Exception as e:
                reply = f"❌ Error:\n\n{e}"

            st.markdown(reply)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )
