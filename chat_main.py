import title_new as title
import chat_remake
from review import *
import streamlit as st
import time



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
            st.session_state.page = "page2"

        elif st.session_state.page == "page2":
        # ここで chat_remake.py のレイアウトを表示
            go_review = []
            go_review = chat_remake.chatpage(st.session_state.start_chat_question)#フラグ，チャット履歴
            
            if go_review[0] == True:
                st.session_state.page == "page3"
        
        elif st.session_state.page == "page3":
            try:
                history = json.loads(user_input)
                review_container(history)
                title_button()
            except json.JSONDecodeError:
                st.error("JSON形式が正しくありません。")
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")

	
    #title_new.pyを使っても文字が返されない






#保留
"""
st.set_page_config(
    page_title="Streamlitでのページ遷移とポップアップボタン",
    layout="wide",
    initial_sidebar_state="expanded"
)








def init():
    if "init" not in st.session_state:
        st.session_state.init=True
        reset_session()
        count()
        return True
    else:
        return False

def count():
    if "count" not in st.session_state:
        st.session_state.count=0
    st.session_state.count+=1

# st.sidebar.selectboxの切り替わりを感知
def tab_session():
    if not st.session_state.now_tab==st.session_state.tab:
        reset_session()
    st.session_state.now_tab=st.session_state.tab

def layer_session(layer=0):
    st.session_state.layer=layer

def reset_session():
    st.session_state.now_tab=None
    layer_session()

init()
st.session_state.ck=0
    
st.session_state.tab = st.sidebar.selectbox("選択してください。", ["Index","List"])
tab_session()# TAB切り替えの管理
# delay
time.sleep(0.1)
#
_tab=st.session_state.tab
_layer=st.session_state.layer
if _tab=="Index":
    if _layer==0 or _layer==1:
        layer_session(1)

elif _tab=="List":
    if _layer==0 or _layer==1:
        layer_session(1)

    elif _layer==2:














"""
if __name__ == "__main__":
    main()



