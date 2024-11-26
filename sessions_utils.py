import streamlit as st



def get_logged_in_username():
    return st.session_state.username if 'username' in st.session_state else ""