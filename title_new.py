import streamlit as st

def display_scenario_selector() -> str:
    """
    研修シナリオを選択し、選択結果を文字列として返す関数。
    """
    st.markdown("## 研修シナリオを選択")

    # シナリオのデータ定義
    scenarios = {
        "顧客対応": "お客様への挨拶、商品説明、クレーム対応など",
        "上司対応": "報告・連絡・相談、会議での発言など",
        "電話応対": "取次ぎ、アポイント調整、問い合わせ対応など",
        "会議・プレゼン": "資料説明、質疑応答、意見交換など"
    }

    # ユーザーが選択したシナリオを保存するための変数
    # 初期値はNoneとし、何も選択されていない状態から始める
    selected_scenario = st.session_state.get("selected_scenario", None)

    # Streamlitの`columns`と`button`を組み合わせて、選択肢をカード風に表示
    cols = st.columns(len(scenarios))
    clicked = False
    for i, (key, value) in enumerate(scenarios.items()):
        with cols[i]:
            # アイコンを定義
            icons = ['👥', '👨‍💼', '📞', '📈']
            icon = icons[i] if i < len(icons) else ''
            
            # ボタンのラベルに絵文字とタイトル、説明を組み込む
            label = f"{icon} **{key}**\n\n{value}"
            
            # ボタンがクリックされたらセッションステートを更新
            if st.button(label, key=f"scenario_btn_{key}", use_container_width=True):
                st.session_state["selected_scenario"] = key
                clicked = True
    
    st.write("---")
    
    # 決定ボタンを配置
    if st.button("決定", use_container_width=True):
        # 決定ボタンが押された時の処理
        if selected_scenario:
            # シナリオが選択されていれば、質問データを生成して返す
            start_question = f"{selected_scenario}のロールプレイを始めましょう。あなたがAIで、私は研修生です。最初の質問をしてください。"
            return start_question
        else:
            # シナリオが選択されていなければ警告メッセージを表示し、Noneを返す
            st.warning("シナリオを選択してください。")
            return None
    
    # ボタンがクリックされただけで再描画するためのリラン
    if clicked:
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
        st.session_state.page = "page1"
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.markdown("<h1 style='text-align: center;'>ビジネスマナー研修アプリ</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>AIとのロールプレイでマナーを身につけよう</p>", unsafe_allow_html=True)
    st.write("---")

    # ページ制御ロジック
    if st.session_state.page == "page1":
        # display_scenario_selectorから返される質問データを受け取る
        start_chat_question = display_scenario_selector()
        
        if start_chat_question:
            # 質問データが返されたらページを遷移
            st.session_state.start_chat_question = start_chat_question
            st.session_state.page = "chat.py"
            st.rerun()

    elif st.session_state.page == "chat.py":
        #以下処理をchat.pyに移動
        return 0

if __name__ == "__main__":
    main()