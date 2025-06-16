# Week 3: Basic App Implementation

Simple app that reads conversations and shows helpful words. Three main parts:

1. `minimal.py` - Backend that:
   - Reads conversation files
   - Gets AI suggestions
   - Saves results to JSON

2. `minimal_gradio.py` - Local UI that:
   - Shows AI responses
   - Shows word suggestions
   - Auto-refreshes every 2 seconds

3. `hf_spaces_app.py` - Similar to minimal_gradio but for Hugging Face and without integrations. It's work in progress. 

## How to Run

1. Install:
```bash
pip install gradio
```

2. Run backend:
```bash
python minimal.py
```

3. Run UI:
```bash
python minimal_gradio.py
```

## Files

```
week3/
├── minimal.py           # Backend - reads conversations, gets AI help
├── minimal_gradio.py    # Local UI
├── hf_spaces_app.py     # Hugging Face UI
├── llm_call.py         # AI helper functions
└── data/               # Conversations and results
```

## Features

- Recording toggle button
- AI response display
- Vocabulary suggestions in three categories:
  - Nouns
  - Adjectives
  - Verbs
- Auto-refresh of suggestions (local version only)