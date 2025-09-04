import title_new as title
import chat
from review import *
#import#ページ4
#import#ページ5
import streamlit as st

"""
class chat_log:
    def __init__(self):
        self.user = "user"
        self.gemini = "gemini"
        # if "chat_log" not in st.session_state:
        #     st.session_state.chat_log = []
        self.chatlog = []
    

    def clear_history(self):
        self.chat_log = []
    
    def add_history(self,chat):
        self.chatlog.append(chat)
"""
    

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
            st.write(start_chat_question)
            # 質問データが返されたらページを遷移
            st.session_state.start_chat_question = start_chat_question
            st.session_state.page = "chat.py"

            go_review = chat.chatpage(st.session_state.start_chat_question)#error
            if go_review == True:
                try:
                    history = json.loads(user_input)
                    review_container(history)
                except json.JSONDecodeError:
                    st.error("JSON形式が正しくありません。")
                except Exception as e:
                    st.error(f"エラーが発生しました: {str(e)}")
    
    #title_new.pyを使っても文字が返されない













if __name__ == "__main__":
    main()



