import title_new as title
import chat
from review import *
import streamlit as st
import log



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
        start_chat_question = title.display_scenario_selector()
        
        if start_chat_question:
                #選択した質問は格納されている
                # 質問データが返されたらページを遷移
            st.session_state.start_chat_question = start_chat_question
            st.session_state.page = "page2"
            st.rerun()


    elif st.session_state.page == "page2":
        chat.chatpage(st.session_state.start_chat_question)#フラグ，チャット履歴

    elif st.session_state.page == "page3":
        try:
            history = chat.get_session_state().messages
            review_container(history)
            title_button()
        except json.JSONDecodeError:
            st.error("JSON形式が正しくありません。")
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
        finally:
            st.session_state.messages = []
            st.success("チャット履歴をリセットしました。")
            st.session_state.page = "page1"
    #追加要素
    elif st.session_state.page == "page4":
        log.log_chat_history(st.session_state.get("chat_history", []))
        if st.button("戻る"):
            st.session_state.page = "page1"
            st.rerun()





if __name__ == "__main__":
    main()



