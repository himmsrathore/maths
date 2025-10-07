import streamlit as st

st.title("jai shree krishna !")  # Adds a title
user_input = st.text_input("Enter your name:")  # Interactive text input
if user_input:
    st.write(f"Hello, {user_input}!")  # Displays dynamic text