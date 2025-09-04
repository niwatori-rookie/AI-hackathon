import streamlit as st
import google.generativeai as genai
import os
import json
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()


# APIキーの設定
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 使用するモデルを選択
model = genai.GenerativeModel('gemini-2.0-flash')

# --- Streamlitのセッションステートを使ってチャット履歴を管理 ---
if 'chat' not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- チャット画面のUI ---
st.title("チャットページ")

# これまでのチャット履歴を表示
for message in st.session_state.chat.history:
    role = "あなた" if message.role == "user" else "Gemini"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# ユーザーからの入力を受け取る
user_prompt = st.chat_input("メッセージを入力してください...")

if user_prompt:
    with st.chat_message("あなた"):
        st.markdown(user_prompt)

    response = st.session_state.chat.send_message(user_prompt)
    with st.chat_message("Gemini"):
        st.markdown(response.text)
    
    # ページを再実行して最新のメッセージを表示
    st.rerun()

# 「やめる」ボタンが押されたときの処理
if st.button("チャットをやめる"):
    # --- ▼▼▼ ここから追加 ▼▼▼ ---
    FILENAME = "log.json"
    
    # 1. 既存のJSONファイルを読み込む
    try:
        with open(FILENAME, 'r', encoding='utf-8') as f:
            all_sessions_data = json.load(f)
        # ファイルが空だったり、形式が違う場合を考慮
        if "sessions" not in all_sessions_data:
            all_sessions_data = {"sessions": []}
    except (FileNotFoundError, json.JSONDecodeError):
        # ファイルが存在しない、または中身が空の場合は、新しいデータ構造を準備
        all_sessions_data = {"sessions": []}

    # 2. 現在のチャット履歴（セッション）を整形する
    current_log_list = []
    for i, msg in enumerate(st.session_state.chat.history):
        #print(i, msg.role, msg.parts[0].text)  # デバッグ用ログ出力
        message_dict = {
            "id": f"{i:03}",
            "speaker": "顧客" if msg.role == "user" else "オペレーター",
            "text": msg.parts[0].text
        }
        current_log_list.append(message_dict)

    # 3. 新しいセッションオブジェクトを作成
    JST = timezone(timedelta(hours=+9))
    session_id_num = len(all_sessions_data["sessions"]) + 1 # 新しいセッションIDを採番
    
    new_session_object = {
        "sessionId": f"session_{session_id_num:03}",
        "timestamp": datetime.now(JST).isoformat(), #修正必要
        "title": "（タイトルはここに格納予定）",
        "summary": "（評価はここに格納予定）",
        "log": current_log_list
    }

    # 4. 読み込んだデータに新しいセッションを追加
    all_sessions_data["sessions"].append(new_session_object)

    # 5. 更新されたデータ全体をJSONファイルに書き込む
    with open(FILENAME, 'w', encoding='utf-8') as f:
        json.dump(all_sessions_data, f, ensure_ascii=False, indent=2)

    st.success(f"チャット履歴を {FILENAME} に保存しました。")

    # ページ３（総評ページ）に遷移
    # st.switch_page("pages/summary.py")