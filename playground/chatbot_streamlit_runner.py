"""Streamlit chatbot"""

import streamlit as st
from genai_voice.bots.chatbot import ChatBot
from genai_voice.logger.log_utils import LogLevels, log


# Initialize the chatbot
chatbot = ChatBot(enable_speakers=True, threaded=True)
history = []


def get_response_audio(audio):
    """Get text response from chatbot"""
    if not audio:
        raise ValueError("No audio file provided.")
    prompt = chatbot.get_prompt_from_gradio_audio(audio)
    log(f"Transcribed prompt: {prompt}", log_level=LogLevels.ON)
    response = chatbot.respond(prompt, history)
    history.append([prompt, response])
    return response


def get_response(user_prmpt):
    """Get text response from chatbot"""
    if not user_prmpt:
        return "Please enter your message."  # Handle empty input

    prompt = user_prmpt
    log(f"User prompt: {prompt}", log_level=LogLevels.ON)
    bot_response = chatbot.respond(prompt, history)
    history.append([prompt, bot_response])
    return bot_response


# Streamlit app layout
st.title("Wanderwise Travel Assistant")

user_audio = chatbot.audio.get_streamlit_audio()
if user_audio:  # returns (sampling_rate, raw_audio_data)
    llm_response = get_response_audio(user_audio)
    if llm_response:
        st.write("Chatbot:", llm_response)
