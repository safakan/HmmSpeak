# HmmSpeak – Week 6: Functional Prototype

This folder contains the **functional prototype** for the HmmSpeak language learning app, developed as part of a 6-week AI app building program. The prototype is implemented as a Flask web application with real-time speech-to-text and AI-powered conversation assistance.

## Overview

**HmmSpeak** helps users practice speaking skills in a new language (English) with real-time conversation partners. When users get stuck, the app provides:
- Related word suggestions (nouns, adjectives, verbs)
- AI-generated response suggestions
- A web interface for conversation and feedback

## Folder Structure

```
week6/
└── HmmSpeakApp/
    ├── hmmspeak-flask/         # Main Flask web app
    │   ├── app/
    │   │   ├── __init__.py     # App factory
    │   │   ├── routes.py       # Main routes and API endpoints
    │   │   ├── utils/
    │   │   │   ├── llm_call.py           # LLM prompt and Together API
    │   │   │   └── transcribe_an_audio.py # Audio transcription Whisper
    │   │   ├── static/
    │   │   │   ├── css/main.css          # UI styles
    │   │   │   └── js/app.js             # Frontend logic
    │   │   └── templates/index.html      # Main web UI
    │   ├── requirements.txt   # Python dependencies
    │   └── run.py             # App entry point
    ├── docker_deployment_backup/
    │   ├── Dockerfile         # Docker setup for deployment
    │   ├── docker_run.py      # Docker run script
    │   └── .dockerignore
    └── dummy.py               # Placeholder file
```

## Functions
- **Real-time audio transcription** using OpenAI Whisper API
- **AI-powered conversation suggestions** (nouns, adjectives, verbs, and a response sentence) via Together API (Llama 3)
- **Web interface** for recording, viewing suggestions, entering custom keywords to guide the conversation, and interacting with the app
- **Docker deployment** support

## Setup & Installation

1. **Clone the repository** and navigate to this folder:
   ```bash
   cd HmmSpeakApp/hmmspeak-flask
   ```

2. **Install Python dependencies** (preferably in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Create a `.env` file in the `hmmspeak-flask` directory with your API keys:
     ```env
     TOGETHER_API_KEY=your_together_api_key
     OPENAI_API_KEY=your_openai_api_key
     ```

## Running the App

- **Locally:**
  ```bash
  python run.py
  ```
  The app will be available at [http://localhost:5000](http://localhost:5000)

- **With Docker:**
  1. Build the image:
     ```bash
     docker build -t hmmspeak-flask .
     ```
  2. Run the container:
     ```bash
     docker run --env-file .env -p 5000:5000 hmmspeak-flask
     ```

## Usage
- Open the web app in your browser.
- Start a conversation and record your speech.
- The app will transcribe your audio and provide:
  - 5 nouns, 5 adjectives, 5 verbs related to your conversation
  - An AI-generated response sentence to help continue the conversation
- Use the suggestions to keep your conversation flowing!
- (Optional) enter keywords to guide the model suggestions

## Notes
- All AI suggestions are generated in English, regardless of the input language.
- If the conversation context is unclear, the AI will provide positive, generic suggestions.
- For development or troubleshooting, check the logs for detailed info on API calls and errors.


## Future directions
- Introduce other languages
- Fine tune a model specific to use case especially for: 
    - Conversations get stuck quite often and need more active support
    - Improve predictive capabilities
    - Simplify suggestions
    - Improve UI 