import streamlit as st
import chat #chat.pyの関数を使うためにインポート


def display_scenario_selector() -> str:
    """
    研修シナリオを選択し、選択結果を文字列として返す関数。
    """

    st.markdown("## 研修シナリオを選択")

    # シナリオのデータ定義
    scenarios = {
        "顧客対応": "お客様への挨拶、商品説明、クレーム対応",
        "上司対応": "報告・連絡・相談、会議での発言",
        "電話応対": "取次ぎ、アポイント調整、問い合わせ対応",
        "会議・プレゼン": "資料説明、質疑応答、意見交換"
    }

    # ユーザーが選択したシナリオを保存するための変数
    # 初期値はNoneとし、何も選択されていない状態から始める
    selected_scenario = st.session_state.get("selected_scenario", None)


    # Streamlitの`columns`と`button`を組み合わせて、選択肢をカード風に表示
    cols = st.columns(len(scenarios))
    clicked = False
    icons = ['👥', '👨‍💼', '📞', '📈']
    for i, (key, value) in enumerate(scenarios.items()):
        with cols[i]:
            icon = icons[i] if i < len(icons) else ''
            label = f"{icon} **{key}**\n\n{value}"
            # 選択されたカードの色を変える
            card_color = "#e6f7ff" if selected_scenario == key else "#f9f9f9"
            st.markdown(f"<div style='background-color:{card_color}; padding:10px; border-radius:0px; display:flex; align-items:center; justify-content:center; height:5px;'>", unsafe_allow_html=True)
            # カードボタンのみ縦長
            card_button_css = """
        <style>
        div[data-testid='stButton'] button.card-btn {
        height: 240px !important;
        font-size: 1.1em;
        white-space: pre-line;
        }
        </style>
                """
            st.markdown(card_button_css, unsafe_allow_html=True)
            if st.button(label, key=f"scenario_btn_{key}", use_container_width=True, help=None, args=None, kwargs=None):
                st.session_state["selected_scenario"] = key
                clicked = True
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("---")
    
    # 決定ボタン用CSS（小さく）
    decision_button_css = """
    <style>
    div[data-testid='stButton'] button.decision-btn {
    height: 40px !important;
    font-size: 1em;
    }
    </style>
    """
    st.markdown(decision_button_css, unsafe_allow_html=True)
    if st.button("決定", key="decision_btn", use_container_width=True):
        if selected_scenario:
            scenario_desc = scenarios[selected_scenario]
            start_question = f"{selected_scenario}（{scenario_desc}）のロールプレイを始めましょう。あなたがAIで、私は研修生です。最初の質問をしてください。"
            return start_question
        else:
            st.warning("シナリオを選択してください。")
            # returnせず、履歴ボタンまで描画
    
    # ボタンがクリックされただけで再描画するためのリラン
    if clicked:
        st.rerun() 
    
    # 履歴ボタン用CSS（小さく）
    history_button_css = """
    <style>
    div[data-testid='stButton'] button.history-btn {
    height: 40px !important;
    font-size: 1em;
    }
    </style>
    """
    st.markdown(history_button_css, unsafe_allow_html=True)
    st.write("")
    if st.button("チャットの履歴を見る", key="history_btn", use_container_width=True):
        st.session_state.page = "history"
        st.rerun()
    return None

def main():
    """
    アプリケーションのメイン関数。
    StreamlitのUIを構築し、ページ遷移を制御します。
    """
    st.set_page_config(layout="wide")

    # セッションステートの初期化
    if "page" not in st.session_state:
        st.session_state.page = "title"
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.markdown("<h1 style='text-align: center;'>ビジネスマナー研修アプリ</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>AIとのロールプレイでマナーを身につけよう</p>", unsafe_allow_html=True)
    st.write("---")

    # ページ制御ロジック
    if st.session_state.page == "title":
        # display_scenario_selectorから返される質問データを受け取る
        start_chat_question = display_scenario_selector()
        if start_chat_question:
            st.session_state.start_chat_question = start_chat_question
            st.session_state.page = "chat.py"
            st.rerun()
    elif st.session_state.page == "chat.py":
        # chat.pyのチャット画面表示関数を呼び出す
        chat.display_chat_page(st.session_state.start_chat_question)
        return 0
    elif st.session_state.page == "history":
        st.markdown("## チャット履歴")
        for i, msg in enumerate(st.session_state.get("chat_history", [])):
            st.write(f"{i+1}: {msg}")
        if st.button("戻る", key="back_btn", use_container_width=True):
            st.session_state.page = "title"
            st.rerun()

if __name__ == "__main__":
    main()