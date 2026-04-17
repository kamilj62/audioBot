import streamlit as st

# Title
st.title("Gradio-like UI")

# Audio input
# st.audio_recorder("Record")
st.text_input("Record")

# Output text
st.text_area("Output")

# Buttons
st.button("Clear")
st.button("Submit")
st.button("Flag")
