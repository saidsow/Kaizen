import streamlit as st
from page1 import display_page as display_page1
from page2 import display_page as display_page2

#Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Intake and Assessment"
if "completed_page1" not in st.session_state:
    st.session_state.completed_page1 = False

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Intake and Assessment", "Your Ideal Self"])

# Navigation logic
if page == "Intake and Assessment":
    display_page1()  # Call Page 1 function

elif page == "Your Ideal Self":
    display_page2()  # Call Page 2 function
