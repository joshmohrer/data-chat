"""Python file to serve as the frontend"""
import streamlit as st
from interface import UI


if __name__ == "__main__":
    st.set_page_config(page_title="AOC Chat Demo",
                       page_icon=":chat:", layout='wide')
    st.header("AOC Chat Demo")

    if "generated" not in st.session_state:
        st.session_state["generated"] = []

    if "past" not in st.session_state:
        st.session_state["past"] = []

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    UI()
