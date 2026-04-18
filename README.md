# AudioBot — GenAI Voice Chatbot

A modular, voice-enabled AI chatbot built with Python, OpenAI, and Gradio. Supports multiple bot personas (travel agent, financial advisor, call center rep, interview coach) with real-time speech-to-text input and text-to-speech responses. Deployed on AWS EC2 via Docker.

> **My Contributions:** Built on an open-source GenAI voice framework. I extended it with an interview coach persona and handled end-to-end deployment to AWS EC2 using Docker — including server setup, swap configuration, containerization, and making the app publicly accessible.

---

## What It Does

- 🎙️ **Speaks and listens** — uses your microphone for input and plays responses through your speakers
- 🤖 **Multiple bot personas** — switch between travel, financial, call center, and interview coach bots via context files
- 🌐 **Web UI** — interactive Gradio interface accessible in the browser
- ☁️ **Cloud deployed** — runs on AWS EC2 (free tier) via Docker
- 🔊 **Flexible audio** — supports OpenAI Whisper API for transcription and gTTS/pyttsx3 for speech output

---

## Demo

![AudioBot UI](assets/image.png)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| LLM | OpenAI GPT-3.5 Turbo |
| Speech-to-Text | OpenAI Whisper API, SpeechRecognition |
| Text-to-Speech | gTTS, pyttsx3 |
| Audio Processing | PyDub, ffmpeg, PyAudio |
| Web UI | Gradio |
| Dependency Management | Poetry |
| Containerization | Docker + Docker Compose |
| Cloud Deployment | AWS EC2 (t2.micro, Free Tier) |

---

## Bot Personas

Each persona is powered by a dedicated context file in the `data/` directory:

| Bot | Context File | Description |
|---|---|---|
| Travel Agent | `travel_bot_context.txt` | Answers travel and itinerary questions |
| Financial Advisor | `financial_bot_context.txt` | Answers financial questions |
| Call Center Rep | `call_center_prompt_with_intents_categories_context.txt` | Handles customer service queries with intent classification |
| Interview Coach | `interview_coach_context.txt` | Helps candidates prep for job interviews |

---

## Project Structure

```
audioBot/
├── app/
│   ├── chatbot_gradio_runner.py      # Main Gradio app entry point
│   └── chatbot_gradio_runner.ipynb   # Jupyter notebook version
├── genai_voice/
│   ├── bots/
│   │   └── chatbot.py                # Core ChatBot class (speak, listen, respond)
│   ├── config/
│   │   └── defaults.py               # API keys, model config
│   ├── data_utils/
│   │   └── extract_web_data.py       # Web scraping utilities for context data
│   ├── defintions/
│   │   ├── prompts.py                # System prompts for each bot persona
│   │   └── model_response_formats.py
│   ├── logger/
│   │   └── log_utils.py              # Custom logging utility
│   ├── models/
│   │   ├── open_ai.py                # OpenAI API wrapper (chat + streaming)
│   │   └── claude_sonnet.py          # Claude model config
│   ├── moderation/
│   │   └── responses.py              # Response filtering
│   └── processing/
│       └── audio.py                  # Audio I/O: mic input, STT, TTS, playback
├── data/                             # Context files for each bot persona
├── playground/                       # Streamlit experiments and audio tests
├── Dockerfile
├── docker-compose.yml
├── aws_deployment_guide.md
└── pyproject.toml
```

---

## Getting Started

### Prerequisites

- Python 3.10 or 3.12
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
- [ffmpeg](https://www.ffmpeg.org/download.html)
- An [OpenAI API key](https://platform.openai.com/docs/quickstart)

### 1. Clone the repo

```bash
git clone https://github.com/kamilj62/audioBot.git
cd audioBot
```

### 2. Install ffmpeg

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
apt install ffmpeg libportaudio2 portaudio19-dev
```

**Windows:** ffmpeg binaries are included in the `libs/` directory.

### 3. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

poetry lock
poetry install
playwright install
```

### 4. Configure environment variables

Create a `.env` file in the root:

```env
OPENAI_API_KEY=your_key_here
USE_LOCAL_WHISPER=False
```

### 5. Run the app

**Option A — Jupyter Notebook:**
```bash
ipython kernel install --user --name=venv
jupyter notebook app/chatbot_gradio_runner.ipynb
```

**Option B — Python script:**
```bash
poetry run RunChatBotScript
```

---

## AWS Deployment

This app is deployed on AWS EC2 (t2.micro free tier) using Docker. See the full step-by-step guide in [`aws_deployment_guide.md`](aws_deployment_guide.md).

**Quick summary:**
1. Launch a t2.micro EC2 instance (Ubuntu)
2. Install Docker on the instance
3. Upload your `.env` file with your OpenAI key
4. Run `docker-compose up -d --build`
5. Access the Gradio UI at `http://your-ec2-public-ip`

> The app uses `USE_LOCAL_WHISPER=False` to offload transcription to OpenAI's API, keeping memory usage low enough to run on the 1GB t2.micro instance.

---

## Tips for Best Results

- Use a headset microphone for cleaner audio capture
- Record in a quiet environment
- Make sure microphone permissions are granted in your browser/OS
- If the build fails on EC2 due to RAM, build the Docker image locally, push to Docker Hub, and pull it on the server

---

## Author

**Joseph Kamil** — AI/ML Engineer based in Los Angeles, CA

- GitHub: [@kamilj62](https://github.com/kamilj62)
- Email: kamilj@umich.edu

---

## License

MIT
