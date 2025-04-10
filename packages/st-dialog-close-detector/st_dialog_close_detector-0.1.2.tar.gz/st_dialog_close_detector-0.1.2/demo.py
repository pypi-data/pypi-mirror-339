import random
import streamlit as st
from st_dialog_close_detector import dialog_close_detector


@st.dialog("my modal")
def my_modal():
    st.write("hi 😊")


if st.button("show modal", key="show-toggle-button"):
    my_modal()

st.write("")
st.write("")
st.write("randon number below will be updated when the dialog is closed")
dialog_close_detector()
st.write("random number: ", random.randint(0, 100))
