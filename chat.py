import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os
from review import *
# import title_new as title

# def _to_gemini_history(messages):#メッセージ履歴をgemini形式に変換
#     history = []
#     for m in st.session_state.notdisplay:
#         role = "user" if m.get("role") == "user" else "model"#非表示部分追加
#         history.append({"role": role, "parts": [m.get("content", "")]})
#     for m in messages:
#         role = "user" if m.get("role") == "user" else "model"#表示部分追加
#         history.append({"role": role, "parts": [m.get("content", "")]})
#     return history

def _to_gemini_history(messages):
    history = []
    
    # 状況を最初に追加
    if st.session_state.situation:
        history.append({
            "role": "user", 
            "parts": [f"会話状況: {st.session_state.situation}"]
        })
    
    for m in messages:
        role = "user" if m.get("role") == "user" else "model"
        history.append({"role": role, "parts": [m.get("content", "")]})
    return history


def _stream_chunks(response):#ストリームチャンクをテキストに変換
    for chunk in response:
        text = getattr(chunk, "text", None)
        if text:
            yield text

def first_chat(prompt):
    st.session_state.situation = prompt

def get_session_state():
    return st.session_state

def reset_session_state():
    st.session_state.messages = []
    st.rerun()

def chatpage(start_question: str):

    st.title("gemini-like clone")

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    if "gemini_model" not in st.session_state:
        st.session_state["gemini_model"] = "gemini-2.0-flash"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "situation" not in st.session_state:
        st.session_state.situation = ""

    # 最初の状況を設定（都度上書きしない）
    if not st.session_state.situation:
        first_chat(start_question)

    if not st.session_state.messages:
        try:
            model = genai.GenerativeModel(st.session_state["gemini_model"])
            chat = model.start_chat(history=_to_gemini_history([]))
            system_prompt = (
                "あなたは会話の相手役です。以下の会話状況に合わせて、"
                "会話を自然に開始する最初の一文だけを、短く、状況に相応しい口調で生成してください。\n"
                f"会話状況: {st.session_state.situation}"
            )
            response = chat.send_message(system_prompt)
            opening_line = getattr(response, "text", "") or "こんにちは。"
            st.session_state.messages.append({"role": "assistant", "content": opening_line})
        except Exception:
            st.session_state.messages.append({"role": "assistant", "content": "こんにちは。"})

    # これまでのメッセージを表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 入力受付
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        model = genai.GenerativeModel(st.session_state["gemini_model"])
        chat = model.start_chat(history=_to_gemini_history(st.session_state.messages[:-1]))

        with st.chat_message("assistant"):
            response_stream = chat.send_message(content=prompt, stream=True)
            final_text = st.write_stream(_stream_chunks(response_stream))

        final_text=st.session_state.messages.append({"role": "assistant", "content": final_text or ""})

    # リセットボタン
    if st.button("やめる"):
        reset_session_state()
        st.success("チャット履歴をリセットしました。")
        st.session_state.page = "page1"
        st.rerun()


    #評価ボタン
    if st.button("評価"):
            st.session_state.final_text = st.session_state.messages
            
            st.session_state.page = "page3"
            
            st.rerun()

            
            


            # try:
            #     history = json.loads(final_text)
            #     review_container(history)
            #     title_button()
            # except json.JSONDecodeError:
            #     st.error("JSON形式が正しくありません。")
            # except Exception as e:
            #     st.error(f"エラーが発生しました: {str(e)}")
            




if __name__ == "__main__":
    chatpage("あなたについて教えてください")