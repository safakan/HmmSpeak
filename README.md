# HmmSpeak for VAM 6 week program, ai app idea building

HmmSpeak helps people practice speaking skills in a new language with real-time conversation partners. The app provides word suggestions and AI responses when users get stuck, helping them continue their conversation naturally.

## How It Works

1. Users start a conversation
2. If they get stuck, they can look at the screen for:
   - Related words (nouns, adjectives, verbs)
   - AI-generated response suggestions
3. Users can either:
   - Use the suggested words to form their own sentences
   - Repeat the AI response to continue the conversation
   - Improvise based on suggestions
   - Guide the conversation manually with custom keyboards

## Data Flow

```
Recording > Transcribe > Conversation Document > LLM > Output Data
```

Output format:
```json
{
    "ai_response": "String",
    "nouns": ["word1", "word2", ...],
    "adjectives": ["word1", "word2", ...],
    "verbs": ["word1", "word2", ...]
}
```

## Repository Structure

- `playground/` - Sandbox area for app-related experiments
- `week1/` - Initial app concept and Gradio UI
- `week2/` - Raw HTML/CSS/JS demo
- `week3/` - Gradio implementation with local and Hugging Face versions
- `week4/` - Flask web app, MCP and RAG implementation
- `week5/` - Basic app demo
- `week6/` - Functional prototype

Each weekly folder contains its own README.md with detailed instructions.

---