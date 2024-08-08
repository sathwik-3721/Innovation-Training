import streamlit as st
from streamlit_option_menu import option_menu

selected = option_menu(
    menu_title=None,
    options=["Home", "About", "Contact"],
    icons=["house", "question", "envelope"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if selected == "Home":
    st.title("Home Page")
if selected == "About":
    st.title("About Page")
if selected == "Contact":
    st.title("Contact Page")