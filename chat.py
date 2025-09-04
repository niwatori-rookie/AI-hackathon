import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

st.title("gemini-like clone")#タイトル表示

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))#APIキー設定

if "gemini_model" not in st.session_state:#モデル選択
    st.session_state["gemini_model"] = "gemini-2.0-flash"

if "messages" not in st.session_state:#メッセージ履歴保存用
    st.session_state.messages = []


msg="あなたは私の上司として振る舞ってください。以後の会話では部下に対する口調で話してください。"


if "notdisplay" not in st.session_state:
    st.session_state.notdisplay = [
        {
            "role": "user", 
            "content": msg
        },
        {
            "role": "assistant", 
            "content": "了解しました。これからはそのように対応したします。"
        }
    ]

for message in st.session_state.messages:#メッセージ履歴表示(場面設定は非表示)
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def _to_gemini_history(messages):#メッセージ履歴をgemini形式に変換
    history = []
    for m in st.session_state.notdisplay:
        role = "user" if m.get("role") == "user" else "model"#非表示部分追加
        history.append({"role": role, "parts": [m.get("content", "")]})
    for m in messages:
        role = "user" if m.get("role") == "user" else "model"#表示部分追加
        history.append({"role": role, "parts": [m.get("content", "")]})
    return history

def _stream_chunks(response):#ストリームチャンクをテキストに変換
    for chunk in response:
        text = getattr(chunk, "text", None)
        if text:
            yield text

if prompt := st.chat_input("What is up?"):#ユーザー入力受付
    st.session_state.messages.append({"role": "user", "content": prompt})#ユーザーのメッセージ履歴追加保存
    with st.chat_message("user"):
        st.markdown(prompt)

    model = genai.GenerativeModel(st.session_state["gemini_model"])
    chat = model.start_chat(history=_to_gemini_history(st.session_state.messages[:-1]))

    with st.chat_message("assistant"):
        response_stream = chat.send_message(prompt, stream=True)
        final_text = st.write_stream(_stream_chunks(response_stream))

    st.session_state.messages.append({"role": "assistant", "content": final_text or ""})#相手のメッセージ履歴を追加保存

if st.button("やめる"):
    st.session_state.messages = []
    st.success("チャット履歴をリセットしました。")
    st.stop()