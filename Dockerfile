# Use a slim Python image
FROM python:3.10-slim

# 1. Install ONLY the absolute bare minimum system tools
RUN apt-get update && apt-get install -y \
    wget \
    xz-utils \
    libportaudio2 \
    portaudio19-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. DOWNLOAD STATIC FFmpeg (Bypasses 100+ heavy libraries!)
RUN wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
    && tar xvf ffmpeg-release-amd64-static.tar.xz \
    && mv ffmpeg-*-amd64-static/ffmpeg /usr/local/bin/ \
    && mv ffmpeg-*-amd64-static/ffprobe /usr/local/bin/ \
    && rm -rf ffmpeg-release-amd64-static.tar.xz ffmpeg-*-amd64-static

# Set working directory
WORKDIR /app

# 3. Fast library install
RUN pip install --no-cache-dir \
    openai \
    speechrecognition \
    soundfile \
    gtts \
    pydub \
    pyaudio \
    pyttsx3 \
    gradio \
    "pydantic<2.10" \
    python-dotenv \
    python-multipart \
    numpy

# Copy the application code
COPY . .

# Expose the Gradio port
EXPOSE 7860

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV USE_LOCAL_WHISPER=False
ENV PYTHONPATH=/app

# Run the application
CMD ["python", "-m", "app.chatbot_gradio_runner"]
