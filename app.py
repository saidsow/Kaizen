import streamlit as st
from page1 import display_page as display_page1
from page2 import display_page as display_page2

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "page1"
if "completed_page1" not in st.session_state:
    st.session_state.completed_page1 = False

# Navigation logic
if st.session_state.page == "page1":
    display_page1()
elif st.session_state.page == "page2":
    display_page2()