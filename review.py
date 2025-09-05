import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os
import json
import pathlib

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def review(history) -> dict:
    """マナー評価を実行する関数
    
    Args:
        history: chat.pyから受け取った会話履歴（{'role': 'user', 'parts': ['内容']}形式）
        
    Returns:
        dict: 評価結果と理由を含む辞書
    """
    model = genai.GenerativeModel("gemini-2.0-flash")
    chat = model.start_chat()
    
    # 履歴を文字列に変換
    conversation_text = ""
    for message in history:
        role = message.get("role", "")
        parts = message.get("content", "")
        content = parts if parts else ""
        conversation_text += f"{role}: {content}\n"
    
    prompt = f"""
あなたはマナー講師です。
この会話は、role"user"がマナーを良くしたいと思っている会話です。
状況は次の通りです。
{history[0]['parts'][0] if history and 'parts' in history[0] else ''}
結果は次の通りです。
{history[1:] if len(history) > 1 else ''}

会話履歴:
{conversation_text}

評価基準:
- 敬語の使用
- 相手への配慮
- コミュニケーションの適切さ
- 礼儀正しさ

"role": "model"のマナーに関しては絶対に評価しないでください。
"role": "user"のマナーに関してのみ非常に厳しく評価してください。
返却値は以下のJSON形式で返してください:
{{
    "result": "A+,A,A-,B+,B,B-,C+,C,C-,D+,D,D-,F",
    "good": ["", ...],
    "bad": ["", ...],
    "title": "会話のタイトル",
    "date": "会話の日付",
}}

評価ランク
- A+: 非常に優秀なマナー
- A: 優秀なマナー
- A-: 良好なマナー
- B+: 良いマナー
- B: 標準的なマナー
- B-: やや改善が必要
- C+: 改善が必要
- C: マナーに問題あり
- C-: マナーに大きな問題
- D+: 非常に問題のあるマナー
- D: 不適切なマナー
- D-: 非常に不適切なマナー
- F: 完全に不適切なマナー
"""
    print(prompt)
    try:
        response = chat.send_message(prompt)
        print(response)
        result = response.text.strip()
        result = result.replace("```json", "").replace("```", "")
        result = json.loads(result)
        return result
    except Exception as e:
        return {
            "result": "評価エラー",
            "reason": f"評価処理中にエラーが発生しました: {str(e)}"
        }

def review_container(history) -> bool:
    """
    マナー評価結果を表示するコンテナ
    
    args:
        history: 会話履歴
        
    return:
        bool: 問題なく処理が完了したか
    """
    if history:
        result = review(history)
    else:
        return False
    with st.container():
        edit_output_json(result)
        st.write("## Geminiからの評価")
        
        st.write("### 良い点")
        for good in result["good"]:
            st.write(f"- {good}")
        st.write("### 悪い点")
        for bad in result["bad"]:
            st.write(f"- {bad}")
        st.write("### 総合評価")
        st.write(result["result"])
    return True

def edit_output_json(result) -> bool:
    """
    出力JSONを編集する関数
    
    args:
        result: 評価結果

    return:
        bool: 問題なく処理が完了したか
    """
    try:
        if pathlib.Path("output.json").exists():
            with open("output.json", "r") as f:
                data = json.load(f)
            data.append(result)
            with open("output.json", "w") as f:
                json.dump(data, f)
        else:
            with open("output.json", "w") as f:
                    json.dump([result], f)
    except Exception as e:
        return False
    return True


def title_button():
    """
    タイトルに戻るボタン

    return:
        bool: 問題なく処理が完了したか
    """
    if st.button("タイトルに戻る"):
        st.session_state.page = "page1"
    return True

if __name__ == "__main__":
    st.title("マナー評価システム")
    
    st.write("このアプリは`chat.py`から会話履歴を受け取ってマナー評価を行います。")
    
    # サンプル履歴でのテスト用
    if st.button("サンプル履歴でテスト"):
        sample_history = [
            {"role": "user", "parts": ["こんにちは、お疲れ様です。"]},
            {"role": "model", "parts": ["こんにちは！お疲れ様です。何かお手伝いできることはありますか？"]},
            {"role": "user", "parts": ["ありがとうございます。資料の件でご相談があります。"]},
            {"role": "model", "parts": ["承知いたしました。どのような資料でしょうか？"]}
        ]
        
        review_container(sample_history)
    
    # 手動で履歴を入力してテストする場合
    st.write("### 手動テスト")
    user_input = st.text_area("会話履歴を入力してください（JSON形式）", 
                             value='[{"role": "user", "parts": ["こんにちは"]}, {"role": "model", "parts": ["こんにちは！"]}]')
    
    if st.button("評価実行"):
        try:
            history = json.loads(user_input)
            review_container(history)
        except json.JSONDecodeError:
            st.error("JSON形式が正しくありません。")
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
    title_button()