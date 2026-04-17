"""Script to run the gradio as code"""

import gradio as gr
import os
from genai_voice.bots.chatbot import ChatBot
from genai_voice.logger.log_utils import log, LogLevels
from genai_voice.defintions.prompts import (
    TRAVEL_AGENT_PROMPT,
    FINANCIAL_PROMPT,
    CALL_CENTER_PROMPT_WITH_INTENTS_CATEGORIES,
    INTERVIEW_COACH_PROMPT
)

# Mapping of UI Role Names to their actual Prompt constants
ROLE_MAPPING = {
    "Travel Agent": TRAVEL_AGENT_PROMPT,
    "Financial Assistant": FINANCIAL_PROMPT,
    "Smart Call Center": CALL_CENTER_PROMPT_WITH_INTENTS_CATEGORIES,
    "Tech Interview Coach": INTERVIEW_COACH_PROMPT
}

# Global cache for bot instances
BOT_INSTANCES = {}

def get_bot(role_name):
    """Lazily initialize and return a bot instance for a specific role"""
    if role_name not in BOT_INSTANCES:
        prompt = ROLE_MAPPING.get(role_name, TRAVEL_AGENT_PROMPT)
        log(f"Initializing new bot instance for: {role_name}", log_level=LogLevels.ON)
        BOT_INSTANCES[role_name] = ChatBot(prompt=prompt, enable_speakers=True, threaded=True)
    return BOT_INSTANCES[role_name]

# Premium CSS for better readability
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

body {
    font-family: 'Inter', sans-serif !important;
}

.gradio-container {
    max-width: 1000px !important;
    margin: 0 auto !important;
}

/* Chat bubble styling */
.chatbot .message.user {
    background-color: var(--primary-600) !important;
    border-radius: 12px 12px 4px 12px !important;
}

.chatbot .message.assistant {
    background-color: var(--background-fill-secondary) !important;
    border-radius: 12px 12px 12px 4px !important;
}

.chatbot .message {
    font-size: 16px !important;
    line-height: 1.6 !important;
    padding: 12px 16px !important;
    margin-bottom: 8px !important;
}

h1 {
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
    margin-bottom: 24px !important;
}

"""

def run():
    """Run Chatbot app with Gradio 6 fixes and premium design"""
    
    def transcribe_and_auto_submit(audio, role_name, history, voice_enabled):
        """Transcribe and immediately trigger the response generator"""
        if not audio:
            return history, ""
        
        bot = get_bot(role_name)
        
        # Use API transcription by default on low-memory environments (AWS Free Tier)
        use_local = os.getenv("USE_LOCAL_WHISPER", "False").lower() == "true"
        text_input = bot.get_prompt_from_gradio_audio(audio, use_api=not use_local)
        
        if not text_input or not text_input.strip():
            log("No speech detected in audio.", log_level=LogLevels.ON)
            return history, ""
            
        log(f"Auto-captured prompt: {text_input}", log_level=LogLevels.ON)
        
        # In Gradio 6, content MUST be a list of blocks
        history.append({
            "role": "user", 
            "content": [{"type": "text", "text": text_input}]
        })
        yield history, ""
        
        # Bot placeholder
        history.append({
            "role": "assistant", 
            "content": [{"type": "text", "text": ""}]
        })
        
        # Convert history for LLM (pull text out of nested blocks)
        llm_history = []
        # Go through valid message pairs in history (User, Assistant)
        # We skip the last message (placeholder) and the current user message (just added)
        for i in range(0, len(history)-2, 2):
            try:
                user_msg = history[i]['content'][0]['text']
                bot_msg = history[i+1]['content'][0]['text']
                llm_history.append([user_msg, bot_msg])
            except (KeyError, IndexError):
                continue
        
        # Stream from bot
        for chunk in bot.respond_stream(text_input, llm_history, enable_voice=voice_enabled):
            history[-1]["content"][0]["text"] += chunk
            yield history, ""

    def get_response_stream(text_input, history, role_name, voice_enabled):
        """Streaming response triggered by manual submit"""
        if not text_input or not text_input.strip():
            yield history, ""
            return
            
        bot = get_bot(role_name)
        
        # Gradio 6 Block Format
        history.append({
            "role": "user", 
            "content": [{"type": "text", "text": text_input}]
        })
        yield history, ""
        
        history.append({
            "role": "assistant", 
            "content": [{"type": "text", "text": ""}]
        })
        
        llm_history = []
        for i in range(0, len(history)-2, 2):
            try:
                user_msg = history[i]['content'][0]['text']
                bot_msg = history[i+1]['content'][0]['text']
                llm_history.append([user_msg, bot_msg])
            except (KeyError, IndexError):
                continue
        
        for chunk in bot.respond_stream(text_input, llm_history, enable_voice=voice_enabled):
            history[-1]["content"][0]["text"] += chunk
            yield history, ""

    def change_role(new_role):
        return [], ""

    # Gradio 6
    with gr.Blocks(title="Audio-Bot: Tech Interview Coach") as demo:
        gr.Markdown("# 🕹️ Interactive AI Assistant")
        
        with gr.Row():
            with gr.Column(scale=2):
                role_dropdown = gr.Dropdown(
                    choices=list(ROLE_MAPPING.keys()),
                    value="Tech Interview Coach",
                    label="Persona",
                    interactive=True
                )
            with gr.Column(scale=1):
                voice_toggle = gr.Checkbox(value=True, label="Speak Aloud")
            with gr.Column(scale=1):
                clear_btn = gr.Button("🗑️ Reset", variant="secondary")

        chat_ui = gr.Chatbot(label="Conversation", height=500, show_label=False)
        
        with gr.Row():
            audio_input = gr.Audio(
                sources=["microphone"], 
                type="numpy", 
                label="Talk",
                interactive=True
            )
            
            with gr.Column(scale=4):
                text_input = gr.Textbox(
                    label="Message", 
                    placeholder="Transcription appears here...", 
                    lines=2,
                    autofocus=True
                )
        
        submit_btn = gr.Button("Send", variant="primary")
        
        role_dropdown.change(fn=change_role, inputs=[role_dropdown], outputs=[chat_ui, text_input])
        clear_btn.click(fn=lambda: ([], ""), outputs=[chat_ui, text_input])

        audio_input.stop_recording(
            fn=transcribe_and_auto_submit,
            inputs=[audio_input, role_dropdown, chat_ui, voice_toggle],
            outputs=[chat_ui, text_input]
        )
        
        submit_btn.click(
            fn=get_response_stream, 
            inputs=[text_input, chat_ui, role_dropdown, voice_toggle], 
            outputs=[chat_ui, text_input]
        )
        
        text_input.submit(
            fn=get_response_stream, 
            inputs=[text_input, chat_ui, role_dropdown, voice_toggle], 
            outputs=[chat_ui, text_input]
        )

    # Configure for server deployment (0.0.0.0)
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False, 
        theme=gr.themes.Soft(),
        css=CSS
    )

# poetry run RunChatBotScript
def run_with_file_support():
    chatbot = ChatBot(enable_speakers=True, threaded=True)
    history = []
    def get_response_from_file(file):
        prompt = chatbot.get_prompt_from_file(file)
        response = chatbot.respond(prompt, history)
        history.append([prompt, response])
        return response
    gr.Interface(get_response_from_file, gr.Audio(sources="microphone", type="filepath"), "text").launch()

if __name__ == "__main__":
    run()
