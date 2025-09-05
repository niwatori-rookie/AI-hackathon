import streamlit as st

def show_chat_history(history):
	"""
	チャット履歴（リスト）を受け取り、画面に表示する関数。
	"""
	st.markdown("## チャット履歴")
	if not history:
		st.info("履歴がありません。")
		return
	for i, msg in enumerate(history):
		st.write(f"{i+1}: {msg}")
