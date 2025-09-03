import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

st.title("gemini-like clone")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = "gemini-2.0-flash"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def _to_gemini_history(messages):
    history = []
    for m in messages:
        role = "user" if m.get("role") == "user" else "model"
        history.append({"role": role, "parts": [m.get("content", "")]})
    return history

def _stream_chunks(response):
    for chunk in response:
        text = getattr(chunk, "text", None)
        if text:
            yield text

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    model = genai.GenerativeModel(st.session_state["gemini_model"])
    chat = model.start_chat(history=_to_gemini_history(st.session_state.messages[:-1]))

    with st.chat_message("assistant"):
        response_stream = chat.send_message(prompt, stream=True)
        final_text = st.write_stream(_stream_chunks(response_stream))

    st.session_state.messages.append({"role": "assistant", "content": final_text or ""})