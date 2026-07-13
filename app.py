import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Offline AI Assistant",
    page_icon="🤖"
)

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

st.title("🤖 Offline AI Assistant")
st.write("Chat with your AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Ask anything...")

if prompt:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    response = model.generate_content(
        prompt + "\nAnswer in 2-3 lines only."
    )

    reply = response.text

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":reply
        }
    )

    with st.chat_message("assistant"):
        st.write(reply)
