import streamlit as st
from st_dialog_close_detector import dialog_close_detector

sess = st.session_state


@st.dialog("my modal", width="large")
def my_modal():
    sess.dialog_toggle = st.toggle(
        "my toggle",
        key="my-toggle",
        value=sess.get("dialog_toggle", False),
    )


if st.button("show modal", key="show-toggle-button"):
    my_modal()

st.write("")
st.write("")
st.write("")
st.write("")
st.write(f"dialog_toggle: {sess.get('dialog_toggle')}")

if st.toggle("enable detector"):
    dialog_close_detector()
